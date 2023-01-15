
import aiohttp
import asyncio
from fastapi import HTTPException
from psycopg import AsyncConnection
from src.readuce.overview import addAIOverview
from src.readuce.utils import fixSideBarListTitle, fixMathFallbackImage
from src.readuce.sub_sections import addAISubSections
from src.wikipedia import data


async def get(
    aconn: AsyncConnection,
    session: aiohttp.ClientSession,
    title: str,
    level: int
):
    soup = await data.getArticleSoup(session, title, level)
    await asyncio.gather(
        addAISubSections(aconn, soup, level, title),
        addAIOverview(aconn, soup, level, title),
    )

    fixSideBarListTitle(soup)
    fixMathFallbackImage(soup)

    if soup.body is not None:
        return soup.body.prettify()

    print("Body not found")
    raise HTTPException(
        status_code=404, detail="Content not found"
    )
