import aiohttp
import json
import openai
import psycopg
import uvicorn
from database import ai_content
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from psycopg.rows import namedtuple_row
from pydantic import BaseModel
from urllib.parse import quote
from readuce import generate, page
from settings import get_settings
from security.leaky_bucket import makeRequest
from utils import logging
# from tasks import genAllLevels
# from tasks import genAllLinks

settings = get_settings()
_http_client_session = None
_pg_connection = None

f = open("manifest.json")
vite_manifest = json.load(f)

openai.api_key = settings.openai_api_key

logger = logging.getMainLogger()

app = FastAPI(root_path="/")

origins = [
    settings.url,
    "http://localhost:5173",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ContentConfig(BaseModel):
    level: int
    title: str
    content_id: str


app.mount("/assets", StaticFiles(directory="assets"), name="assets")

templates = Jinja2Templates(directory="templates")


def log_notice(diag):
    print(f"The server says: {diag.severity} - {diag.message_primary}")


async def getPGConnection():
    global _pg_connection
    if _pg_connection is None:
        _pg_connection = await psycopg.AsyncConnection.connect(
            host=settings.postgres_host,
            dbname=settings.postgres_db,
            user=settings.postgres_user,
            password=settings.postgres_pass,
            row_factory=namedtuple_row)
        _pg_connection.add_notice_handler(log_notice)
    return _pg_connection


async def getHTTPClientSession():
    global _http_client_session
    if _http_client_session is None:
        _http_client_session = aiohttp.ClientSession()
    return _http_client_session


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html.j2", {
            "request": request,
            "stylesheet": vite_manifest["index.css"]["file"],
            "main": vite_manifest["index.html"]["file"],
        }

        # "index.dev.html.j2",
        # {
        #     "request": request,
        # }
    )


@app.get("/wiki/{title:path}", response_class=HTMLResponse)
async def wiki(request: Request):
    return templates.TemplateResponse(
        # "index.html.j2",
        # {
        #     "request": request,
        #     "stylesheet": vite_manifest["index.css"]["file"],
        #     "main": vite_manifest["index.html"]["file"],
        # }
        "index.dev.html.j2",
        {
            "request": request,
        })


@app.get("/api/wiki/{level}/{title:path}", response_class=HTMLResponse)
async def generate_page(request: Request, level: int, title: str):
    title = quote(title, safe='')
    print(f'title is: {title}')
    ip = "all"
    if request.client is not None:
        ip = request.client.host

    aconn = await getPGConnection()
    if await makeRequest(aconn, ip, 1):
        session = await getHTTPClientSession()

        html = await page.aGet(session, title)
        # genAllLevels.delay(html, title)
        # genAllLinks.delay(html, level)
        return html

    raise HTTPException(status_code=403, detail="Too many requests")


@app.post("/api/wiki/content", response_class=JSONResponse)
async def get_content(request: Request, config: ContentConfig):
    ip = "all"
    if request.client is not None:
        ip = request.client.host

    aconn = await psycopg.AsyncConnection.connect(
        host=settings.postgres_host,
        dbname=settings.postgres_db,
        user=settings.postgres_user,
        password=settings.postgres_pass,
        row_factory=namedtuple_row)
    aconn.add_notice_handler(log_notice)

    if await makeRequest(aconn, ip, 1):
        session = await getHTTPClientSession()
        openai.aiosession.set(session)

        id = config.content_id
        if id != "readuce":
            id = id[3:]

        await ai_content.aCreateTitleTable(aconn, config.level, config.title)

        row = await ai_content.aGet(aconn, config.level, config.title, id)

        if row is None:

            # If we are generating the overview, not a sub section
            if id == "readuce":
                row = await generate.aOverview(
                    aconn,
                    config.level,
                    config.title,
                )

            else:
                row = await generate.aSubSection(
                    aconn,
                    config.level,
                    config.title,
                    id,
                )

        if row is not None:
            return {
                "content": row.content,
                "model": row.model,
                "timestamp": row.timestamp
            }

        logger.error("Unable to get content")
        raise HTTPException(status_code=500, detail="Unable to get content")

    raise HTTPException(status_code=403, detail="Too many requests")


@app.get("/redirect")
async def redirect():
    response = RedirectResponse(url='/redirected')
    return response


@app.get("/test/tasks/{title:path}", response_class=HTMLResponse)
async def test_tasks(request: Request, title: str):
    title = quote(title, safe='')
    print(f'title is: {title}')
    ip = "all"
    if request.client is not None:
        ip = request.client.host

    aconn = await getPGConnection()
    if await makeRequest(aconn, ip, 1):
        session = await getHTTPClientSession()
        openai.aiosession.set(session)
        html = await page.aGet(session, title)
        # genAllLevels.delay(html, title)
        # genAllLinks.delay(html, 1)
        return html

    raise HTTPException(status_code=403, detail="Too many requests")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",  # type: ignore
        host=settings.host,
        port=4000,
        workers=4)
