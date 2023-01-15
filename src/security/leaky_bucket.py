from typing import Optional
from psycopg import sql, AsyncConnection
from settings import get_settings
from psycopg.rows import TupleRow


settings = get_settings()

# Number of requests allowed per time period
TOKEN_LIMIT = settings.leaky_bucket_token_limit
# Length of time period in seconds
TIME_WINDOW = settings.leaky_bucket_time_window


async def createIPTable(aconn: AsyncConnection, ip: str):

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


async def getTokenCount(aconn: AsyncConnection, ip: str):
    await createIPTable(aconn, ip)

    async with aconn.cursor() as acur:

        # Get the current number of tokens in the bucket
        await acur.execute(sql.SQL(
            '''
            SELECT SUM(token_count)
            FROM leaky_bucket.{ip}
            WHERE token_timestamp > NOW() - INTERVAL '{window} seconds'
            '''
        ).format(ip=sql.Identifier(ip), window=TIME_WINDOW))

        requests = 0
        fetch: Optional[TupleRow] = await acur.fetchone()

        if fetch is not None:
            if fetch.sum is not None:
                requests = fetch.sum
        print(f"Requests in last {TIME_WINDOW // 60} minutes: {requests}")

        # The remaining number of tokens for the time period
        remaining = TOKEN_LIMIT - requests

        print(f"Requests remaining: {remaining}")

        return remaining


async def addTokens(aconn: AsyncConnection, ip: str, count: int):
    # Add the specified number of tokens to the bucket
    await aconn.execute(sql.SQL(
        '''
        INSERT INTO leaky_bucket.{ip} (token_timestamp, token_count)
        VALUES (NOW(), {count})
        '''
    ).format(ip=sql.Identifier(ip), count=count))

    await aconn.commit()


async def makeRequest(aconn: AsyncConnection, ip: str, count: int):
    print(f"IP is {ip}")
    # Check if there are enough tokens in the bucket to make the request
    token_count = await getTokenCount(aconn, ip)

    if token_count >= count:
        await addTokens(aconn, ip, count)
        return True
    else:
        # Not enough tokens in the bucket, so return False
        return False
