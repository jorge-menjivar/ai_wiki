from database.leaky_bucket import aCreateIPTable, aAdd, aGet
from psycopg import AsyncConnection
from settings import get_settings


settings = get_settings()

# Number of requests allowed per time period
TOKEN_LIMIT = settings.leaky_bucket_token_limit
# Length of time period in seconds
TIME_WINDOW = settings.leaky_bucket_time_window


async def makeRequest(aconn: AsyncConnection, ip: str, count: int):
    print(f"IP is {ip}")
    await aCreateIPTable(aconn, ip)
    # Check if there are enough tokens in the bucket to make the request
    requests = 0
    fetch = await aGet(aconn, ip, TIME_WINDOW)
    if fetch is not None:
        if fetch.sum is not None:
            requests = fetch.sum
    print(f"Requests in last {TIME_WINDOW // 60} minutes: {requests}")

    # The remaining number of tokens for the time period
    remaining = TOKEN_LIMIT - requests

    print(f"Requests remaining: {remaining}")

    if remaining >= count:
        await aAdd(aconn, ip, count)
        return True
    else:
        # Not enough tokens in the bucket, so return False
        return False
