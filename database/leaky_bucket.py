from psycopg import sql, AsyncConnection

from utils import logging

logger = logging.getMainLogger()


async def aGetTokens(aconn: AsyncConnection, ip: str, time_window):
    """
    aGetTokens(aconn, ip, time_window)

    Asynchronously get the number of tokens from a 'leaky_bucket' within a
    given time window.

    Parameters
    ----------
    aconn : psycopg.AsyncConnection
        Asynchronous connection to a PostgreSQL database.
    ip : string
        The IP address associated with the bucket.
    time_window : int
        Time window in seconds to get the sum of tokens from the bucket.

    Returns
    -------
    fetch : scalar
        The number of token within the given time window.

    Raises
    ------
    psycopg.errors.DataError
        SQL syntax errors, data errors (e.g. invalid IP format).
    psycopg.errors.OperationalError
        Database errors (e.g. incorrect database schema).
    """

    # Get the current number of tokens in the bucket
    acur = await aconn.execute(
        sql.SQL('''
        SELECT SUM(token_count)
        FROM security.leaky_bucket
        WHERE ip = {ip}
        AND timestamp > NOW() - INTERVAL '{window} seconds'
        ''').format(ip=ip, window=time_window))

    fetch = await acur.fetchone()

    await aconn.commit()

    return fetch


async def aAddTokens(aconn: AsyncConnection, ip: str, count: int):
    """
    aAddTokens(aconn, ip, count)

    Asynchronously add the specified number of tokens to the 'leaky_bucket'.

    Parameters
    ----------
    aconn : psycopg.AsyncConnection
        Asynchronous connection to a PostgreSQL database.
    ip : string
        The IP address associated with the bucket.
    count : int
        The number of tokens to add to the bucket.

    Returns
    -------
    None

    Raises
    ------
    psycopg.errors.DataError
        SQL syntax errors, data errors (e.g. invalid IP format).
    psycopg.errors.IntegrityError
        Unique constraint violations (e.g. inserting duplicate entries).
    psycopg.errors.OperationalError
        Database errors (e.g. incorrect database schema).
"""

    # Add the specified number of tokens to the bucket
    await aconn.execute(
        '''
        INSERT INTO security.leaky_bucket (ip, timestamp, token_count)
        VALUES (%s, NOW(), %s)
        ''', (ip, count))

    await aconn.commit()
