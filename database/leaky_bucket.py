from typing import Optional
from psycopg import sql, AsyncConnection
from psycopg.rows import TupleRow


async def aCreateIPTable(aconn: AsyncConnection, ip: str):

    # Create the table to store the tokens if it doesn't already exist
    await aconn.execute(sql.SQL(
        '''
        CREATE TABLE IF NOT EXISTS leaky_bucket.{ip} (
            token_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
            token_count INTEGER NOT NULL
        )
        '''
    ).format(ip=sql.Identifier(ip)))

    await aconn.commit()


async def aGet(aconn: AsyncConnection, ip: str, time_window):

    async with aconn.cursor() as acur:

        # Get the current number of tokens in the bucket
        await acur.execute(sql.SQL(
            '''
            SELECT SUM(token_count)
            FROM leaky_bucket.{ip}
            WHERE token_timestamp > NOW() - INTERVAL '{window} seconds'
            '''
        ).format(ip=sql.Identifier(ip), window=time_window))

        fetch: Optional[TupleRow] = await acur.fetchone()

        return fetch


async def aAdd(aconn: AsyncConnection, ip: str, count: int):
    # Add the specified number of tokens to the bucket
    await aconn.execute(sql.SQL(
        '''
        INSERT INTO leaky_bucket.{ip} (token_timestamp, token_count)
        VALUES (NOW(), {count})
        '''
    ).format(ip=sql.Identifier(ip), count=count))

    await aconn.commit()
