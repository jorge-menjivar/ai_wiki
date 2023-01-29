import asyncio
import aiohttp
from bs4 import BeautifulSoup
from fastapi import HTTPException
from readuce.overview import aAddAIOverview, addAIOverview
from readuce.sub_sections import aAddAISubSections, addAISubSections
from readuce.utils import fixSideBarListTitle, fixMathFallbackImage
from readuce.utils import includeTitle
from wikipedia import data


async def aGet(session: aiohttp.ClientSession, title: str):
    soup = await data.aGetArticleSoup(session, title)
    await asyncio.gather(
        aAddAISubSections(soup),
        aAddAIOverview(soup),
    )

    fixSideBarListTitle(soup)
    fixMathFallbackImage(soup)
    includeTitle(soup)

    if soup.body is not None:
        page = BeautifulSoup(f"<div>{soup.body}</div>", 'html.parser')
        return page.prettify()

    print("Body not found")
    raise HTTPException(status_code=404, detail="Content not found")


def get(title: str):
    soup = data.getArticleSoup(title)

    addAISubSections(soup)
    addAIOverview(soup)

    fixSideBarListTitle(soup)
    fixMathFallbackImage(soup)

    if soup.body is not None:
        return soup.body.prettify()

    print("Body not found")
    raise HTTPException(status_code=404, detail="Content not found")
