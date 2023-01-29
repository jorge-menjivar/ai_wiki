from datetime import datetime, timezone
from typing import Optional
from utils import logging, parsing
from psycopg import sql, AsyncConnection
from psycopg import ProgrammingError, IntegrityError
from psycopg.rows import TupleRow
from psycopg.types.json import Jsonb

logger = logging.getMainLogger()


async def aGetContent(
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
        SELECT sections[{section}]
        FROM {table}
        WHERE title = {title}
        ''').format(
            table=sql.Identifier(parsing.getLevelString(level), "contents"),
            title=title,
            section=section,
        ))

    section_data: None | dict[str, str] = None

    try:
        fetch = await acur.fetchone()

        if fetch is not None:
            section_data = fetch[0]

    except ProgrammingError:
        logger.error("ERROR DURING FETCH")

    if commit:
        try:
            await aconn.commit()

        except IntegrityError:
            logger.warning("ROLLING BACK")
            await aconn.rollback()

    return section_data


async def aAddContent(
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

    timestamp = str(datetime.now(timezone.utc))

    update_data = {'content': content, 'model': model, 'timestamp': timestamp}
    new_row_data = {section: update_data}

    # Add the content to a new section in the database
    acur = await aconn.execute(
        sql.SQL('''
        INSERT INTO {table} (title, sections)
        VALUES ({title}, {new_row_data})
        ON CONFLICT (title)
        DO UPDATE
        SET sections[{section}] = {content}
        RETURNING sections[{section}]
        ''').format(
            table=sql.Identifier(parsing.getLevelString(level), "contents"),
            title=title,
            new_row_data=Jsonb(new_row_data),
            section=section,
            content=Jsonb(update_data),
        ))

    section_data: None | dict[str, str] = None

    try:
        fetch: Optional[TupleRow] = await acur.fetchone()

        if fetch is not None:
            section_data = fetch[0]

    except ProgrammingError:
        logger.error("ERROR DURING FETCH")

    if commit:
        try:
            await aconn.commit()

        except IntegrityError:
            logger.warning("ROLLING BACK")
            await aconn.rollback()

    return section_data
