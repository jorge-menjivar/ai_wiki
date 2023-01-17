from typing import Optional
from psycopg import sql, AsyncConnection
from psycopg.rows import TupleRow


async def __createTitleTable(aconn: AsyncConnection, level: int, title: str):

    # Create the table to store ai generated content if it doesn't exist
    await aconn.execute(sql.SQL(
        '''
        CREATE TABLE IF NOT EXISTS {table} (
            "section" varchar PRIMARY KEY NOT NULL,
            "content" varchar NOT NULL,
            "model" varchar NOT NULL,
            "timestamp" TIMESTAMP WITHOUT TIME ZONE NOT NULL
        );
        '''
    ).format(table=sql.Identifier(__getLevelString(level), title)))

    await aconn.commit()


async def get(
    aconn: AsyncConnection,
    level: int,
    title: str,
    section: str
):
    await __createTitleTable(aconn, level, title)

    # Get the section content for a specific title
    acur = await aconn.execute(sql.SQL(
        '''
        SELECT *
        FROM {table}
        WHERE section = {section}
        '''
    ).format(
        table=sql.Identifier(__getLevelString(level), title),
        section=section)
    )

    fetch: Optional[TupleRow] = await acur.fetchone()

    return fetch


async def update(
    aconn: AsyncConnection,
    level: int,
    title: str,
    section: str,
    content: str,
    model: str
):

    await aconn.execute(sql.SQL(
        '''
        UPDATE {table}
        SET "content"={content}, "model"={model}, "timestamp"=NOW()
        WHERE "section"={section};
        '''
    ).format(
        table=sql.Identifier(__getLevelString(level), title),
        section=section,
        content=content,
        model=model
    ))

    await aconn.commit()


async def add(
    aconn: AsyncConnection,
    level: int,
    title: str,
    section: str,
    content: str,
    model: str,
):

    # Add the content to a new section in the database
    acur = await aconn.execute(sql.SQL(
        '''
        INSERT INTO {table} (section, content, model, timestamp)
        VALUES ({section}, {content}, {model}, NOW())
        ON CONFLICT (section) DO NOTHING
        RETURNING *
        '''
    ).format(
        table=sql.Identifier(__getLevelString(level), title),
        section=section,
        content=content,
        model=model
    ))

    fetch: Optional[TupleRow] = await acur.fetchone()
    await aconn.commit()

    return fetch


def __getLevelString(level: int):
    level_string: str = f"l{level}"
    return level_string
