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
    """
    Parameters
    ----------
    aconn : AsyncConnection
        Async connection to the database.
    level : int
        The level at which the content should be retrieved.
    title : str
        Title of the content.
    section : str
        Section of the content to be retrieved.
    commit : bool, optional
        If `True`, the changes in the database made by the function are
        committed.
        The default is `True`.

    Returns
    -------
    section_data : None | dict[str, str]
        Dict containing the content of the specified section, if found and
        `None` otherwise.

    Raises
    ...
        If an error is encountered during the fetching of data.
    IntegrityError
        If an integrity problem is encountered and a rollback is made.
    """

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
    """
    Parameters
    ----------
    aconn: AsyncConnection
        An asynchronous connection to a PostgreSQL database.
    level: int
        The level of the section the content is being added to.
    title: str
        The title of the content.
    section: str
        The name of the section to add the content to.
    content: str
        The content to be added to the section.
    model: str
        The model type of the content.
    commit: bool, optional
        Whether or not to commit changes to the database. Default is True.

    Returns
    -------
    section_data: None | dict[str, str]
    ...
        If there was an error when fetching the new section data.
    IntegrityError:
        If there was an error when committing the changes to the database.
    """

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
