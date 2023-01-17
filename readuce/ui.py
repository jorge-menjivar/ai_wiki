from bs4 import BeautifulSoup
from fastapi import Request
from fastapi.templating import Jinja2Templates
from settings import get_settings
from readuce.utils import removeItalics

settings = get_settings()

templates = Jinja2Templates(directory="templates")


def addUI(request: Request, soup: BeautifulSoup):
    if soup.body is not None and soup.title is not None:
        return templates.TemplateResponse(
            "content.html.j2",
            {
                "request": request,
                "title": removeItalics(soup.title.string),
                "ui_title": soup.title.string,
                "content": soup.body.prettify()
            }
        )


def addTestUI(request: Request, soup: BeautifulSoup):
    if soup.body is not None and soup.title is not None:
        return templates.TemplateResponse(
            "test.html.j2",
            {
                "request": request,
            }
        )
