import logging
import openai
import psycopg
from bs4 import BeautifulSoup
from celery import Celery
from celery.app.log import TaskFormatter
from celery.signals import after_setup_task_logger
from celery.utils.log import get_task_logger
from psycopg.rows import namedtuple_row
from database import ai_content
from readuce import generate
from readuce.utils import removeUnderscores
from settings import get_settings
from wikipedia import data
from openai.util import logger as openai_logger

settings = get_settings()

openai.api_key = settings.openai_api_key
openai_logger.disabled = True

logger = get_task_logger(__name__)

worker = Celery('tasks', broker='redis://localhost:6379/0')


def psql_log_notice(diag):
    if diag.severity == "NOTICE":
        pass
        # logger.info(f"POSTGRESQL: - {diag.message_primary}")
    elif diag.severity == "WARNING":
        logger.warning(f"POSTGRESQL: - {diag.message_primary}")
    else:
        logger.error(f"POSTGRESQL: - {diag.severity} - {diag.message_primary}")


def newPSQLConnection():
    psql_conn = psycopg.connect(
        host=settings.postgres_host,
        dbname=settings.postgres_db,
        user=settings.postgres_user,
        password=settings.postgres_pass,
        row_factory=namedtuple_row,
    )

    psql_conn.add_notice_handler(psql_log_notice)

    return psql_conn


@after_setup_task_logger.connect
def setup_task_logger(logger, *args, **kwargs):
    # for handler in logger.root.handlers:
    #     handler.setFormatter(TaskFormatter('%(levelname)s - %(message)s'))
    #     # TaskFormatter(
    #     #     '%(asctime)s - %(task_id)s - %(task_name)s - %(name)s - %(levelname)s - %(message)s'
    #     # )

    for handler in logger.handlers:
        handler.setFormatter(
            TaskFormatter('%(task_name)s - %(levelname)s - %(message)s'))
        # TaskFormatter(
        #     '%(asctime)s - %(task_id)s - %(task_name)s - %(name)s - %(levelname)s - %(message)s'
        # )


@worker.task
def genAIOverview(
    level: int,
    title: str,
):
    conn = newPSQLConnection()
    # logger.info(f"Generating level {level} overview for {title}")
    generate.overview(conn, level, title)


@worker.task
def genAISubSection(level: int, title: str, sub_section: str, id: str):
    #     logger.info(f"""\
    # Generating level {level} section summary {title} --- {sub_section}\
    # """)

    conn = newPSQLConnection()
    generate.subSection(conn, level, title, sub_section, id)


@worker.task
def genAllLinks(html: str, level: int, genLevels: bool = False):
    soup = BeautifulSoup(html, 'html.parser')

    if soup.body is not None:
        body = soup.body
        links = body.find_all('a')
        unique_titles = []
        skipped_titles = []
        for a in links:
            keys: list = a.attrs.keys()
            if 'rel' in keys:
                rel: str = a['rel']
                if 'mw:WikiLink' in rel:
                    site_url_len = len(settings.url)
                    title: str = a['href'][site_url_len + 10:]

                    if (title.find(':') == -1):
                        # and title[:5] != "Help:"
                        # and title[:7] != "Portal:"
                        # and title[:8] != "Special:"
                        # and title[:9] != "Template:"
                        # and title[:14] != "Template_talk:"

                        i_params = title.find('?')
                        i_sect = title.find('#')

                        if i_params != -1:
                            title = title[:i_params]

                        if i_sect != -1:
                            title = title[:i_sect]

                        if title not in unique_titles:
                            unique_titles.append(title)

                    else:
                        skipped_titles.append(title)

        # unique_titles.sort()
        for title in unique_titles:
            logger.info(title)
            if genLevels:
                genTitleAndLevels.delay(title)
            else:
                genTitle.delay(title, level)

        # logger.info(f'total links {len(links)}')

        # logger.info(f'total unique links {len(unique_titles)}')

        # skipped_titles.sort()
        # logger.info("SKIPPED TITLES")
        # for title in skipped_titles:
        #     logger.info(title)

    return True


@worker.task
def genAllLevels(html: str, title: str):

    conn = newPSQLConnection()
    soup = BeautifulSoup(html, 'html.parser')

    for level in range(1, settings.max_levels + 1):
        ai_content.createTitleTable(conn, level, title)

        row = ai_content.get(conn, level, title, "readuce")

        if row is None:
            genAIOverview.delay(level, title)

        if soup.body is not None:

            ss_tags = soup.body.find_all('h3')

            for i, ss_tag in enumerate(ss_tags):

                id = ss_tag['id']

                row = ai_content.get(conn, level, title, section=id)

                if row is None:

                    sub_section: str = removeUnderscores(id)

                    genAISubSection.delay(level, title, sub_section, id)


@worker.task
def genTitle(title: str, level: int):

    conn = newPSQLConnection()
    logger.debug(f'GENERATING TITLE: {title}, LEVEL: {level}')

    soup = data.getArticleSoup(title, level)

    ai_content.createTitleTable(conn, level, title)

    logger.debug('GETTING OVERVIEW')
    row = ai_content.get(conn, level, title, "readuce")
    logger.debug('GOT OVERVIEW')

    if row is None:

        logger.debug('GENERATING OVERVIEW')
        generate.overview(conn, level, title)
        logger.debug('GENERATED OVERVIEW')

    if soup.body is not None:

        ss_tags = soup.body.find_all('h3')

        for i, ss_tag in enumerate(ss_tags):

            id = ss_tag['id']

            logger.debug(f'GETTING SUB-SECTION {id}')
            row = ai_content.get(conn, level, title, section=id)
            logger.debug(f'GOT SUB-SECTION {id}')

            if row is None:

                sub_section: str = removeUnderscores(id)

                logger.debug(f'GENERATING SUB-SECTION: {id}')
                generate.subSection(
                    conn,
                    level,
                    title,
                    sub_section,
                    id,
                )
                logger.debug('GENERATED SUB-SECTION')

    logger.info(f'GENERATED TITLE: {title}, LEVEL: {level}')


@worker.task
def genTitleAndLevels(title: str):

    conn = newPSQLConnection()
    soup = data.getArticleSoup(title, 0)

    for level in range(1, settings.max_levels + 1):
        ai_content.createTitleTable(conn, level, title)

        row = ai_content.get(conn, level, title, "readuce")

        if row is None:
            genAIOverview.delay(level, title)

        if soup.body is not None:

            ss_tags = soup.body.find_all('h3')

            for i, ss_tag in enumerate(ss_tags):

                id = ss_tag['id']

                row = ai_content.get(conn, level, title, section=id)

                if row is None:

                    sub_section: str = removeUnderscores(id)

                    genAISubSection.delay(level, title, sub_section, id)
