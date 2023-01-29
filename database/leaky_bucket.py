from psycopg import sql, AsyncConnection

from utils import logging

logger = logging.getMainLogger()


async def aGetTokens(aconn: AsyncConnection, ip: str, time_window):

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
    # Add the specified number of tokens to the bucket
    await aconn.execute(
        '''
        INSERT INTO security.leaky_bucket (ip, timestamp, token_count)
        VALUES (%s, NOW(), %s)
        ''', (ip, count))

    await aconn.commit()
