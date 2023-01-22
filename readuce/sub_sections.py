import asyncio
from bs4 import BeautifulSoup
from database import ai_content
from psycopg import AsyncConnection, Connection
from readuce import generate
from readuce.utils import removeUnderscores


async def aAddAISubSections(
    aconn: AsyncConnection,
    soup: BeautifulSoup,
    level: int,
    title: str,
):
    if soup.body is not None:

        await ai_content.aCreateTitleTable(aconn, level, title)

        ss_tags = soup.body.find_all('h3')

        for ss_tag in ss_tags:

            id = ss_tag['id']
            print(id)

            row = await ai_content.aGet(aconn, level, title, section=id)

            content: str = ""
            if row is None:
                sub_section: str = removeUnderscores(id)

                asyncio.create_task(
                    generate.aSubSection(aconn, level, title, sub_section, id)
                )

            else:
                content = row.content

                tag = BeautifulSoup(
                    f"""{ss_tag}\
                    <div class='ai_sub_section'>\
                        <p>{content}</p>\
                    </div>""",
                    'html.parser'
                )

                ss_tag.replace_with(tag)


def addAISubSections(
    conn: Connection,
    soup: BeautifulSoup,
    level: int,
    title: str,
):

    if soup.body is not None:

        ai_content.createTitleTable(conn, level, title)

        ss_tags = soup.body.find_all('h3')

        for ss_tag in ss_tags:

            id = ss_tag['id']
            print(id)

            row = ai_content.get(conn, level, title, section=id)

            content: str = ""
            if row is None:
                sub_section: str = removeUnderscores(id)

                generate.subSection(conn, level, title, sub_section, id)

            else:
                content = row.content

                tag = BeautifulSoup(
                    f"""{ss_tag}\
                    <div class='ai_sub_section'>\
                        <p>{content}</p>\
                    </div>""",
                    'html.parser'
                )

                ss_tag.replace_with(tag)
