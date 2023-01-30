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
    """
    makeRequest(aconn, ip, count)

    Parameters
    ----------
    aconn : AsyncConnection
        An asynchronous connection to the Postgres database.
    ip : str
        The IP address of the client making the request.
    count : int
        The number of requests being made by the client.

    Returns
    -------
    bool
        A boolean value indicating whether the request was allowed.

    Notes
    -----
    This function is used to check whether a client has enough tokens in the
    leaky bucket to make a request. If the IP address is 127.0.0.1, the
    request is always allowed. Otherwise, the remaining tokens are checked
    against the count. If there are enough tokens, they are removed from the
    bucket and the request is allowed. If not, the request is denied.
    """

    # Check if there are enough tokens in the bucket to make the request
    requests = 0
    fetch = await aGetTokens(aconn, ip, TIME_WINDOW)
    if fetch is not None:
        if fetch.sum is not None:
            requests = fetch.sum

    # The remaining number of tokens for the time period
    remaining = TOKEN_LIMIT - requests

    logger.info(f"{ip} --- {requests} / {TOKEN_LIMIT}")

    # Allowing localhost to make unlimited requests
    if remaining >= count or ip == "127.0.0.1":
        await aAddTokens(aconn, ip, count)
        return True
    else:
        # Not enough tokens in the bucket, so return False
        return False
