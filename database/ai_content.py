from celery.utils.log import get_task_logger
from typing import Optional
from psycopg import sql, AsyncConnection, Connection
from psycopg import ProgrammingError, IntegrityError
from psycopg.rows import TupleRow

logger = get_task_logger(__name__)


async def aCreateTitleTable(
    aconn: AsyncConnection,
    level: int,
    title: str,
    commit: bool = True,
):

    title = title.lower()

    # Create the table to store ai generated content if it doesn't exist
    await aconn.execute(
        sql.SQL('''
        CREATE TABLE IF NOT EXISTS {table} (
            "section" varchar PRIMARY KEY NOT NULL,
            "content" varchar NOT NULL,
            "model" varchar NOT NULL,
            "timestamp" TIMESTAMP WITHOUT TIME ZONE NOT NULL
        );
        ''').format(table=sql.Identifier(__getLevelString(level), title)))

    if commit:
        try:
            await aconn.commit()

        except IntegrityError:
            logger.warning("ROLLING BACK")
            await aconn.rollback()


async def aGet(
    aconn: AsyncConnection,
    level: int,
    title: str,
    section: str,
    commit: bool = True,
):

    title = title.lower()
    section = section.lower()

    # Get the section content for a specific title
    acur = await aconn.execute(
        sql.SQL('''
        SELECT *
        FROM {table}
        WHERE section = {section}
        ''').format(table=sql.Identifier(__getLevelString(level), title),
                    section=section))

    fetch = None

    try:
        fetch: Optional[TupleRow] = await acur.fetchone()

    except ProgrammingError:
        logger.error("ERROR DURING FETCH")

    if commit:
        try:
            await aconn.commit()

        except IntegrityError:
            logger.warning("ROLLING BACK")
            await aconn.rollback()

    return fetch


async def aUpdate(
    aconn: AsyncConnection,
    level: int,
    title: str,
    section: str,
    content: str,
    model: str,
    commit: bool = True,
):

    title = title.lower()
    section = section.lower()

    await aconn.execute(
        sql.SQL('''
        UPDATE {table}
        SET "content"={content}, "model"={model}, "timestamp"=NOW()
        WHERE "section"={section};
        ''').format(table=sql.Identifier(__getLevelString(level), title),
                    section=section,
                    content=content,
                    model=model))

    if commit:
        try:
            await aconn.commit()

        except IntegrityError:
            logger.warning("ROLLING BACK")
            await aconn.rollback()


async def aAdd(
    aconn: AsyncConnection,
    level: int,
    title: str,
    section: str,
    content: str,
    model: str,
    commit: bool = True,
):

    title = title.lower()
    section = section.lower()

    # Add the content to a new section in the database
    acur = await aconn.execute(
        sql.SQL('''
        INSERT INTO {table} (section, content, model, timestamp)
        VALUES ({section}, {content}, {model}, NOW())
        ON CONFLICT (section) DO NOTHING
        RETURNING *
        ''').format(table=sql.Identifier(__getLevelString(level), title),
                    section=section,
                    content=content,
                    model=model))

    fetch = None

    try:
        fetch: Optional[TupleRow] = await acur.fetchone()

    except ProgrammingError:
        logger.error("ERROR DURING FETCH")

    if commit:
        try:
            await aconn.commit()

        except IntegrityError:
            logger.warning("ROLLING BACK")
            await aconn.rollback()

    return fetch


def createTitleTable(
    conn: Connection,
    level: int,
    title: str,
    commit: bool = True,
):

    title = title.lower()

    # Create the table to store ai generated content if it doesn't exist
    conn.execute(
        sql.SQL('''
        CREATE TABLE IF NOT EXISTS {table} (
            "section" varchar PRIMARY KEY NOT NULL,
            "content" varchar NOT NULL,
            "model" varchar NOT NULL,
            "timestamp" TIMESTAMP WITHOUT TIME ZONE NOT NULL
        );
        ''').format(table=sql.Identifier(__getLevelString(level), title)))

    if commit:
        try:
            conn.commit()
            logger.debug('CREATE TABLE: SUCCESS')
            return True

        except IntegrityError:
            logger.debug('CREATE TABLE: FAILED')
            logger.warning("ROLLING BACK")
            conn.rollback()
            return False


def get(
    conn: Connection,
    level: int,
    title: str,
    section: str,
    commit: bool = True,
):

    title = title.lower()
    section = section.lower()

    # Get the section content for a specific title
    cur = conn.execute(
        sql.SQL('''
        SELECT *
        FROM {table}
        WHERE section = {section}
        ''').format(table=sql.Identifier(__getLevelString(level), title),
                    section=section))

    fetch = None

    try:
        fetch: Optional[TupleRow] = cur.fetchone()
        logger.debug('FETCH: SUCCESS')

    except ProgrammingError:
        logger.debug('FETCH: FAILED')
        logger.error("ERROR DURING FETCH IN GET")

    if commit:
        try:
            conn.commit()
            logger.debug('GET CONTENT: SUCCESS')

        except IntegrityError:
            logger.debug('GET CONTENT: FAILED')
            logger.warning("ROLLING BACK")
            conn.rollback()
    return fetch


def update(
    conn: Connection,
    level: int,
    title: str,
    section: str,
    content: str,
    model: str,
    commit: bool = True,
):

    title = title.lower()
    section = section.lower()

    conn.execute(
        sql.SQL('''
        UPDATE {table}
        SET "content"={content}, "model"={model}, "timestamp"=NOW()
        WHERE "section"={section};
        ''').format(table=sql.Identifier(__getLevelString(level), title),
                    section=section,
                    content=content,
                    model=model))

    if commit:
        try:
            conn.commit()

        except IntegrityError:
            logger.warning("ROLLING BACK")
            conn.rollback()


def add(
    conn: Connection,
    level: int,
    title: str,
    section: str,
    content: str,
    model: str,
    commit: bool = True,
):

    title = title.lower()
    section = section.lower()

    logger.debug(f"conn: {conn}")
    logger.debug(f"level: {level}")
    logger.debug(f"title: {title}")
    logger.debug(f"section: {section}")
    logger.debug(f"content: {content}")
    logger.debug(f"model: {model}")

    # Add the content to a new section in the database
    cur = conn.execute(
        sql.SQL('''
        INSERT INTO {table} (section, content, model, timestamp)
        VALUES ({section}, {content}, {model}, NOW())
        ON CONFLICT (section) DO NOTHING
        RETURNING *
        ''').format(table=sql.Identifier(__getLevelString(level), title),
                    section=section,
                    content=content,
                    model=model))

    fetch = None

    try:
        fetch: Optional[TupleRow] = cur.fetchone()
        logger.debug('RETURN FETCH: SUCCESS')

    except ProgrammingError:
        logger.debug('RETURN FETCH: FAILED')
        logger.error("ERROR DURING FETCH IN ADD")

    if commit:
        try:
            conn.commit()
            logger.debug('ADD CONTENT: SUCCESS')

        except IntegrityError:
            logger.debug('ADD CONTENT: FAILED')
            logger.warning("ROLLING BACK")
            conn.rollback()

    return fetch


def __getLevelString(level: int):
    level_string: str = f"l{level}"
    return level_string
