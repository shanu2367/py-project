
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import qrcode
import os

app = FastAPI()

os.makedirs("static/qr_codes", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"qr": None}
    )


@app.get("/generate", response_class=HTMLResponse)
async def generate(request: Request, url: str):

    qr = qrcode.make(url)

    with open("static/qr_codes/qr.png", "wb") as qr_file:
        qr.save(qr_file)
        

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"qr": "/static/qr_codes/qr.png"}
    )
