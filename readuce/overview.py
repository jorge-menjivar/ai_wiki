import asyncio
from bs4 import BeautifulSoup
from database import ai_content
from psycopg import AsyncConnection, Connection
from readuce import generate


async def aAddAIOverview(aconn: AsyncConnection, soup: BeautifulSoup,
                         level: int, title: str):

    if soup.body is not None:

        await ai_content.aCreateTitleTable(aconn, level, title)

        row = await ai_content.aGet(aconn, level, title, "readuce")

        content: str = ""
        model: str = ""
        timestamp: str = ""
        if row is None:
            asyncio.create_task(generate.aOverview(aconn, level, title))

        else:
            content = row.content
            model = row.model
            timestamp = row.timestamp

            first_p = soup.body.find('p')

            disclaimer = f'''This content was generated using {model} on \
                {timestamp}'''

            tag = BeautifulSoup(
                f'''<h2>Overview</h2>
                        <div class="ai_overview">
                            <p class="overview_disclaimer">{disclaimer}</p>
                            <p class="overview_content">{content}</p>
                        </div>
                    <h2>Article</h2> {first_p}''', 'html.parser')

            if first_p is not None:
                first_p.replace_with(tag)


def addAIOverview(conn: Connection, soup: BeautifulSoup, level: int,
                  title: str):

    if soup.body is not None:

        ai_content.createTitleTable(conn, level, title)

        row = ai_content.get(conn, level, title, "readuce")

        content: str = ""
        model: str = ""
        timestamp: str = ""
        if row is None:
            generate.overview(conn, level, title)

        else:
            content = row.content
            model = row.model
            timestamp = row.timestamp

            first_p = soup.body.find('p')

            disclaimer = f'''This content was generated using {model} on \
                {timestamp}'''

            tag = BeautifulSoup(
                f'''<h2>Overview</h2>
                        <div class="ai_overview">
                            <p class="overview_disclaimer">{disclaimer}</p>
                            <p class="overview_content">{content}</p>
                        </div>
                    <h2>Article</h2> {first_p}''', 'html.parser')

            if first_p is not None:
                first_p.replace_with(tag)
