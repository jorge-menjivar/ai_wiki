import aiohttp
import requests
from settings import getSettings
from bs4 import BeautifulSoup

settings = getSettings()


async def aGetArticleSoup(session: aiohttp.ClientSession, title: str):
    # Downloading data for title

    url = f'https://en.wikipedia.org/api/rest_v1/page/html/{title}'

    headers = {
        "accept":
        """text/html; charset=utf-8;\
profile='https://www.mediawiki.org/wiki/Specs/HTML/2.1.0'"""
    }

    async with session.get(url, headers=headers) as response:

        html = await response.text()

        soup = BeautifulSoup(html, 'html.parser')

        # Update links
        for a in soup.find_all('a'):
            keys: list = a.attrs.keys()
            if 'rel' in keys:
                rel: str = a['rel']
                if 'mw:WikiLink' in rel:
                    old_link = a['href']
                    new_link = f"//{settings.url}/wiki/" + old_link[2:]
                    a['href'] = new_link

        # Removed injected styles
        if soup.head is not None:
            for style in soup.find_all('style'):
                style.decompose()

        __removeAMBoxes(soup)

        return soup


def getArticleSoup(title: str):
    # Downloading data for title

    url = f'https://en.wikipedia.org/api/rest_v1/page/html/{title}'

    headers = {
        "accept":
        """text/html; charset=utf-8;\
profile='https://www.mediawiki.org/wiki/Specs/HTML/2.1.0'"""
    }

    response = requests.get(url, headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Update links
    for a in soup.find_all('a'):
        keys: list = a.attrs.keys()
        if 'rel' in keys:
            rel: str = a['rel']
            if 'mw:WikiLink' in rel:
                old_link = a['href']
                new_link = f"//{settings.url}/wiki/" + old_link[2:]
                a['href'] = new_link

    # Removed injected styles
    if soup.head is not None:
        for style in soup.find_all('style'):
            style.decompose()

    __removeAMBoxes(soup)

    return soup


def getMobile(title: str):
    # Downloading data for title

    url = f'https://en.wikipedia.org/api/rest_v1/page/segments/{title}'

    headers = {"accept": "application/json"}
    response = requests.get(url, headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    for a in soup.find_all('a'):
        keys: list = a.attrs.keys()
        if 'rel' in keys:
            rel: str = a['rel']
            if 'mw:WikiLink' in rel:
                old_link = a['href']
                new_link = f"//{settings.url}/wiki/" + old_link[2:]
                a['href'] = new_link

    return soup.prettify()


def getResource(res_path: str):

    url = f'https://en.wikipedia.org/w/{res_path}'

    response = requests.get(url)

    return response.text


def __removeAMBoxes(soup: BeautifulSoup):
    if soup.body is not None:
        for t in soup.body.find_all('table', attrs={'class': 'ambox'}):
            t.decompose()

    return soup
