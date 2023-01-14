from typing import Optional
from psycopg import sql, Connection
from psycopg.rows import TupleRow


def createTitleTable(conn: Connection, level: int, title: str):

    # Create the table to store ai generated content if it doesn't exist
    conn.execute(sql.SQL(
        '''
        CREATE TABLE IF NOT EXISTS {table} (
            "section" varchar PRIMARY KEY NOT NULL,
            "content" varchar NOT NULL,
            "model" varchar NOT NULL,
            "timestamp" TIMESTAMP WITHOUT TIME ZONE NOT NULL
        );
        '''
    ).format(table=sql.Identifier(__getLevelString(level), title)))

    conn.commit()


def getContentRow(conn: Connection, level: int, title: str, section: str):
    createTitleTable(conn, level, title)

    # Get the section content for a specific title
    cursor = conn.execute(sql.SQL(
        '''
        SELECT *
        FROM {table}
        WHERE section = {section}
        '''
    ).format(
        table=sql.Identifier(__getLevelString(level), title),
        section=section)
    )

    fetch: Optional[TupleRow] = cursor.fetchone()

    return fetch


def updateContent(
    conn: Connection,
    level: int,
    title: str,
    section: str,
    content: str,
    model: str
):

    conn.execute(sql.SQL(
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

    conn.commit()


def addContent(
    conn: Connection,
    level: int,
    title: str,
    section: str,
    content: str,
    model: str,
):

    # Add the content to a new section in the database
    cursor = conn.execute(sql.SQL(
        '''
        INSERT INTO {table} (section, content, model, timestamp)
        VALUES ({section}, {content}, {model}, NOW())
        RETURNING *
        '''
    ).format(
        table=sql.Identifier(__getLevelString(level), title),
        section=section,
        content=content,
        model=model
    ))

    fetch: Optional[TupleRow] = cursor.fetchone()
    conn.commit()

    return fetch


def __getLevelString(level: int):
    level_string: str = f"l{level}"
    return level_string
