from fastapi import FastAPI, File, Form, UploadFile
from app import get_phrase_from_words, get_words
from io import BytesIO
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import aiohttp
import aiofiles
from pathlib import Path


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

path = Path(__file__).parent



@app.get('/')
async def homepage():
    html_content = (path / 'index.html').open().read()
    return HTMLResponse(content=html_content, status_code=200)


@app.post("/analyze")
async def analyze(file: bytes = File(...)):
    pred = get_phrase_from_words(get_words(BytesIO(file)))
    return {"result": pred}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
