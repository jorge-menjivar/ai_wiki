from psycopg import sql, Connection


def createTitleTable(conn: Connection, level: int, title: str):

    # Create the table to store ai generated content if it doesn't exist
    conn.execute(sql.SQL(
        '''
        CREATE TABLE IF NOT EXISTS {table} (
            "section" varchar PRIMARY KEY NOT NULL,
            "content" varchar NOT NULL
        );
        '''
    ).format(table=sql.Identifier(__getLevelString(level), title)))

    conn.commit()


def getContent(conn: Connection, level: int, title: str, section: str):
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

    content: str | None = None
    fetch = cursor.fetchone()

    if fetch is not None:
        if fetch[0] is not None:
            content = fetch[1]

    print(f"Content fetched: {content}")

    return content


def updateContent(
    conn: Connection,
    level: int,
    title: str,
    section_name: str,
    content: str
):

    conn.execute(sql.SQL(
        '''
        UPDATE {table}
        SET "content"={content}
        WHERE "section"={section};
        '''
    ).format(
        table=sql.Identifier(__getLevelString(level), title),
        section_name=section_name,
        content=content
    ))

    conn.commit()


def addContent(
    conn: Connection,
    level: int,
    title: str,
    section_name: str,
    content: str
):

    # Add the content to a new section in the database
    conn.execute(sql.SQL(
        '''
        INSERT INTO {table} (section, content)
        VALUES ({section_name}, {content})
        '''
    ).format(
        table=sql.Identifier(__getLevelString(level), title),
        section_name=section_name,
        content=content
    ))

    conn.commit()


def __getLevelString(level: int):
    level_string: str = f"l{level}"
    return level_string
