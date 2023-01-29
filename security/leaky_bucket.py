from database.leaky_bucket import aAddTokens, aGetTokens
from psycopg import AsyncConnection
from settings import getSettings
from utils import logging

settings = getSettings()
logger = logging.getMainLogger()

# Number of requests allowed per time period
TOKEN_LIMIT = settings.leaky_bucket_token_limit
# Length of time period in seconds
TIME_WINDOW = settings.leaky_bucket_time_window


async def makeRequest(aconn: AsyncConnection, ip: str, count: int):
    logger.info(f"Source: {ip}")
    # Check if there are enough tokens in the bucket to make the request
    requests = 0
    fetch = await aGetTokens(aconn, ip, TIME_WINDOW)
    if fetch is not None:
        if fetch.sum is not None:
            requests = fetch.sum
    logger.info(f"Requests in last {TIME_WINDOW // 60} minutes: {requests}")

    # The remaining number of tokens for the time period
    remaining = TOKEN_LIMIT - requests

    logger.info(f"Requests remaining: {remaining}")

    if remaining >= count:
        await aAddTokens(aconn, ip, count)
        return True
    else:
        # Not enough tokens in the bucket, so return False
        return False
