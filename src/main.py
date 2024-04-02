from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate

from additional_info.router import router as router_information


app = FastAPI(
    title="Digital portfolio"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.mount("/static/css", StaticFiles(directory="static/css"), name="static_css")
app.mount("/static/js", StaticFiles(directory="static/js"), name="static_js")
app.mount("/static/image", StaticFiles(directory="static/image"), name="static_image")

templates = Jinja2Templates(directory="static/html")

@app.get("/login", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


app.include_router(router_information)
