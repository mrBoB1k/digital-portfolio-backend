from typing import Annotated
from fastapi import APIRouter, Depends, Request

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Path, Query

from auth.base_config import current_user
from auth.models import User


router = APIRouter()

templates = Jinja2Templates(directory="static/html")

@router.get("/login", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def read_register(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@router.get("/", response_class=HTMLResponse)
async def read_headpage(request: Request):
    return templates.TemplateResponse("headpage.html", {"request": request})


@router.get("/profile/{user_id}", response_class=HTMLResponse, name="profile")
async def read_profile(
    request: Request,
    user_id: Annotated[int, Path(title="The ID of the user")]):
    return templates.TemplateResponse("profile.html", {"request": request})

@router.get("/my_profile", response_class=RedirectResponse)
async def ling_to_my_profile(
    request: Request,
    user: User = Depends(current_user)
):
    profile_url = request.url_for("profile", user_id=user.id)
    return RedirectResponse(url=str(profile_url))

@router.get("/search", response_class=HTMLResponse)
async def read_register(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})