import json
import openai
import psycopg
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pipeline import PipelineCloud
from urllib.parse import quote
from settings import get_settings
from src.readuce.overview import addAIOverview
# from src.readuce.sections import addAISections
from src.readuce.sub_sections import addAISubSections
from src.security.leaky_bucket import makeRequest
from src.wikipedia import data

settings = get_settings()

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

# Connect to the database
conn = psycopg.connect(
    host=settings.postgres_host,
    dbname=settings.postgres_db,
    user=settings.postgres_user,
    password=settings.postgres_pass,
)

api = PipelineCloud(token=settings.mystic_api_token)
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
async def render_page(request: Request, level: int, title: str):
    print(f'title is: {title}')
    title = quote(title, safe='')
    print(f'title is: {title}')
    ip = "all"
    if request.client is not None:
        ip = request.client.host

    if makeRequest(conn, ip, 1):
        soup = data.getArticleSoup(title, level)
        addAISubSections(conn, soup, level, title)
        addAIOverview(conn, soup, level, title)

        if soup.body is not None:
            return soup.body.prettify()

        print("Body not found")
        raise HTTPException(
            status_code=404, detail="Content not found"
        )

    else:
        print("Request denied")
        raise HTTPException(
            status_code=429, detail="Limit reached. Try again in a few minutes"
        )


@app.get("/mobile/{title}", response_class=HTMLResponse)
async def render_mobile(request: Request, title: str):
    ip = "all"
    if request.client is not None:
        ip = request.client.host

    if makeRequest(conn, ip, 1):
        page = data.getMobile(title)
        return page

    else:
        print("Request denied")
        raise HTTPException(
            status_code=429, detail="Limit reached. Try again in a few minutes"
        )


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
