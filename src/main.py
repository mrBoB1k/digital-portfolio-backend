from fastapi import FastAPI
from fastapi.params import Depends
from fastapi.staticfiles import StaticFiles


from auth.base_config import auth_backend, fastapi_users, current_user
from auth.models import User
from auth.schemas import UserRead, UserCreate

from additional_info.router import router as router_information
from database import DATABASE_URL
from page_router import router as router_page

from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI(
    title="Digital portfolio"
)

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)


@app.get("/auth/is_authenticated", tags=["Auth"])
def is_authenticated(user: User = Depends(current_user)):
    if user:
        return True
    else:
        return False



app.mount("/static", StaticFiles(directory="static"), name="static")

app.mount("/static/css", StaticFiles(directory="static/css"), name="static_css")
app.mount("/static/js", StaticFiles(directory="static/js"), name="static_js")
app.mount("/static/image", StaticFiles(directory="static/image"), name="static_image")

app.include_router(router_page)

app.include_router(router_information)



origins = [
    "http://192.168.1.181:8000",
    "http://localhost:5432",
    DATABASE_URL,
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    # allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    # allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
    #                "Authorization", "Access-Control-Allow-Credentials", "Vary", "Accept", "Connection",
    #                 "Referer", "Host", "User-Agent", "Accept-Language", "Accept-Encoding", "content-type",
    #                 "Referrer Policy", "Authorization", "Authorizations", "APIKeyCookie", "apiKey", "authorizations",
    #                 "bonds", "cookie", "In", "Name", "Value"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.add_middleware(
#         CORSMiddleware,
#         allow_origins=origins,
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     ),