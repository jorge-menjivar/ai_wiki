import asyncio
from bs4 import BeautifulSoup
from database import ai_content
from psycopg import AsyncConnection, Connection
from readuce import generate


async def aAddAISubSections(
    aconn: AsyncConnection,
    soup: BeautifulSoup,
    level: int,
    title: str,
):
    if soup.body is not None:

        await ai_content.aCreateTitleTable(aconn, level, title)

        ss_tags = soup.body.find_all('h3')

        for ss_tag in ss_tags:

            id = ss_tag['id']
            print(id)

            row = await ai_content.aGet(aconn, level, title, section=id)

            if row is None:

                asyncio.create_task(
                    generate.aSubSection(aconn, level, title, id))

            tag = BeautifulSoup(
                f"""{ss_tag}\
                <div class='ai_sub_section' id='ai_{id}'>
                </div>""", 'html.parser')

            ss_tag.replace_with(tag)


def addAISubSections(
    conn: Connection,
    soup: BeautifulSoup,
    level: int,
    title: str,
):

    if soup.body is not None:

        ai_content.createTitleTable(conn, level, title)

        ss_tags = soup.body.find_all('h3')

        for ss_tag in ss_tags:

            id = ss_tag['id']
            print(id)

            row = ai_content.get(conn, level, title, section=id)

            if row is None:

                generate.subSection(conn, level, title, id)

            tag = BeautifulSoup(
                f"""{ss_tag}\
                <div class='ai_sub_section'>
                </div>""", 'html.parser')

            ss_tag.replace_with(tag)
