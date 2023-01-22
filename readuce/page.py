
import aiohttp
import asyncio
from fastapi import HTTPException
from psycopg import AsyncConnection, Connection
from readuce.overview import aAddAIOverview, addAIOverview
from readuce.utils import fixSideBarListTitle, fixMathFallbackImage
from readuce.sub_sections import aAddAISubSections, addAISubSections
from wikipedia import data


async def aGet(
    aconn: AsyncConnection,
    session: aiohttp.ClientSession,
    title: str,
    level: int
):
    soup = await data.aGetArticleSoup(session, title, level)
    await asyncio.gather(
        aAddAISubSections(aconn, soup, level, title),
        aAddAIOverview(aconn, soup, level, title),
    )

    fixSideBarListTitle(soup)
    fixMathFallbackImage(soup)

    if soup.body is not None:
        return soup.body.prettify()

    print("Body not found")
    raise HTTPException(
        status_code=404, detail="Content not found"
    )


def get(
    conn: Connection,
    title: str,
    level: int
):
    soup = data.getArticleSoup(title, level)

    addAISubSections(conn, soup, level, title)
    addAIOverview(conn, soup, level, title)

    fixSideBarListTitle(soup)
    fixMathFallbackImage(soup)

    if soup.body is not None:
        return soup.body.prettify()

    print("Body not found")
    raise HTTPException(
        status_code=404, detail="Content not found"
    )
