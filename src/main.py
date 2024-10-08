from fastapi import FastAPI
from fastapi.params import Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from auth.base_config import auth_backend, fastapi_users, current_user
from auth.models import User
from auth.schemas import UserRead, UserCreate

from additional_info.router import router as router_information
from page_router import router as router_page
from download.download_router import router as router_download
from download.download_router import router2 as router_avatar
from search.router import router as router_search
from subscription.router import router as router_sub

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
async def is_authenticated(user: User = Depends(current_user)):
    if user:
        return True
    else:
        return False



app.mount("/static", StaticFiles(directory="static"), name="static")

app.mount("/static/css", StaticFiles(directory="static/css"), name="static_css")
app.mount("/static/js", StaticFiles(directory="static/js"), name="static_js")
app.mount("/static/image", StaticFiles(directory="static/image"), name="static_image")
app.mount("/static/fonts", StaticFiles(directory="static/fonts"), name="static_fonts")


app.include_router(router_page)

app.include_router(router_information)

app.include_router(router_download)

app.include_router(router_avatar)

app.include_router(router_search)

app.include_router(router_sub)


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")