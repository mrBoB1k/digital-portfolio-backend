from fastapi import APIRouter, Request

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()



templates = Jinja2Templates(directory="static/html")

@router.get("/login", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@router.get("/", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("headpage.html", {"request": request})


@router.get("/profile", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})