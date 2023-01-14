from psycopg import sql, Connection
from settings import get_settings


settings = get_settings()

# Number of requests allowed per time period
TOKEN_LIMIT = settings.leaky_bucket_token_limit
# Length of time period in seconds
TIME_WINDOW = settings.leaky_bucket_time_window


def createIPTable(conn: Connection, ip: str):

    # Create the table to store the tokens if it doesn't already exist
    conn.execute(sql.SQL(
        '''
        CREATE TABLE IF NOT EXISTS leaky_bucket.{ip} (
            token_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
            token_count INTEGER NOT NULL
        )
        '''
    ).format(ip=sql.Identifier(ip)))

    conn.commit()


def getTokenCount(conn: Connection, ip: str):
    createIPTable(conn, ip)

    # Get the current number of tokens in the bucket
    cursor = conn.execute(sql.SQL(
        '''
        SELECT SUM(token_count)
        FROM leaky_bucket.{ip}
        WHERE token_timestamp > NOW() - INTERVAL '{window} seconds'
        '''
    ).format(ip=sql.Identifier(ip), window=TIME_WINDOW))

    requests = 0
    fetch = cursor.fetchone()

    if fetch is not None:
        requests = fetch.sum
    print(f"Requests in last {TIME_WINDOW // 60} minutes: {requests}")

    remaining = TOKEN_LIMIT - requests

    print(f"Requests remaining: {remaining}")

    return remaining


def addTokens(conn: Connection, ip: str, count: int):
    # Add the specified number of tokens to the bucket
    conn.execute(sql.SQL(
        '''
        INSERT INTO leaky_bucket.{ip} (token_timestamp, token_count)
        VALUES (NOW(), {count})
        '''
    ).format(ip=sql.Identifier(ip), count=count))

    conn.commit()


def makeRequest(conn: Connection, ip: str, count: int):
    print(f"IP is {ip}")
    # Check if there are enough tokens in the bucket to make the request
    token_count = getTokenCount(conn, ip)

    if token_count >= count:
        addTokens(conn, ip, count)
        conn.commit()
        return True
    else:
        # Not enough tokens in the bucket, so return False
        return False
