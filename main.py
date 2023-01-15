import aiohttp
import asyncio
import json
import openai
import psycopg
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from psycopg.rows import namedtuple_row
from urllib.parse import quote
from settings import get_settings
from src.readuce import page
from src.security.leaky_bucket import makeRequest
from src.wikipedia import data

settings = get_settings()
_http_client_session = None
_pg_connection = None

f = open("manifest.json")
vite_manifest = json.load(f)

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
            row_factory=namedtuple_row
        )
        _pg_connection.add_notice_handler(log_notice)
    return _pg_connection


async def getHTTPClientSession():
    global _http_client_session
    if _http_client_session is None:
        _http_client_session = aiohttp.ClientSession()
    return _http_client_session


# api = PipelineCloud(token=settings.mystic_api_token)s
openai.api_key = settings.openai_api_key


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        # "index.html.j2",
        # {
        #     "request": request,
        #     "stylesheet": vite_manifest["index.css"].file,
        #     "main": vite_manifest["index.js"].file,
        # }

        "index.dev.html.j2",
        {
            "request": request,
        }
    )


@app.get("/wiki/{level}/{title:path}", response_class=HTMLResponse)
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
        }
    )


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
        openai.aiosession.set(session)
        return await page.get(aconn, session, title, level)

    raise HTTPException(
        status_code=403, detail="Too many requests"
    )


async def test():
    await asyncio.sleep(5)
    return {"slept": True}


@app.get("/wait", response_class=JSONResponse)
async def wait_json(request: Request):

    print("Wait request received")

    task = test()

    res = {}
    for f in asyncio.as_completed([task]):
        res = await f
    return res


@app.get("/w/{res_path:path}", response_class=HTMLResponse)
async def stylesheet(request: Request, res_path: str):
    res = data.getResource(res_path)
    return res


if __name__ == "__main__":
    uvicorn.run(
        app,  # type: ignore
        host=settings.host,
        port=4000,
    )
