from psycopg import sql, Connection
from psycopg import IntegrityError
from psycopg.rows import namedtuple_row
from utils import logging, parsing
from settings import getSettings

settings = getSettings()
logger = logging.getMainLogger()

conn = Connection.connect(
    host=settings.postgres_host,
    dbname=settings.postgres_db,
    user=settings.postgres_user,
    password=settings.postgres_pass,
    row_factory=namedtuple_row,
)

setup = False


def setupDatabase():
    """
    Sets up the PostgreSQL database for the application.

    Parameters
    ----------
    None

    Returns
    -------
    None

    """

    global setup
    if setup is False:
        setup = True
        logger.info('SETTING UP DATABASE')
        __createSchemas(conn)
        __createTables(conn)


def __createSchemas(conn: Connection):

    # Create a schema for each level
    for i in range(1, settings.max_levels + 1):
        conn.execute(
            sql.SQL('''
            CREATE SCHEMA IF NOT EXISTS {schema};
            ''').format(schema=sql.Identifier(parsing.getLevelString(i))))

    # Create a cache schema
    conn.execute('''CREATE SCHEMA IF NOT EXISTS cache;''')

    # Create a security schema
    conn.execute('''CREATE SCHEMA IF NOT EXISTS security;''')

    try:
        conn.commit()
        logger.info('SUCCESS - CREATE SCHEMAS')

    except IntegrityError:
        logger.error('FAILURE - CREATE SCHEMAS')
        logger.warning("ROLLING BACK")
        conn.rollback()


def __createTables(conn: Connection):

    # Create a table for each level to store ai generated contents
    for i in range(1, settings.max_levels + 1):
        conn.execute(
            sql.SQL('''
            CREATE TABLE IF NOT EXISTS {table} (
                "title" varchar PRIMARY KEY NOT NULL,
                "sections" jsonb NOT NULL
            );
            ''').format(
                table=sql.Identifier(parsing.getLevelString(i), "contents")))

    # Create table to store wikipedia pages inside cache schema
    conn.execute('''
        CREATE TABLE IF NOT EXISTS cache.pages (
            "title" varchar PRIMARY KEY NOT NULL,
            "soup" varchar NOT NULL
        );
        ''')

    # Create table to leaky_bucket data inside the security schema
    conn.execute('''
        CREATE TABLE IF NOT EXISTS security.leaky_bucket (
            "ip" varchar NOT NULL,
            "timestamp" TIMESTAMP WITH TIME ZONE NOT NULL,
            "token_count" INTEGER NOT NULL
        );
        ''')

    try:
        conn.commit()
        logger.info('SUCCESS - CREATE TABLES')

    except IntegrityError:
        logger.error('FAILURE - CREATE TABLES')
        logger.warning("ROLLING BACK")
        conn.rollback()
