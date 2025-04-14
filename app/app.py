from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers.url import router as url_router
from app.routers.history import router as history_router
from app.db import create_db_and_tables
from fastapi import Depends, FastAPI
from app.db import User
from app.schemas import UserCreate, UserRead, UserUpdate
from app.users import auth_backend, current_active_user, fastapi_users
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan, redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.allowed_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)


app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


app.include_router(url_router, prefix="/api/urls", tags=["urls"])
app.include_router(history_router, prefix="/api", tags=["history"])


@app.get("/")
def read_root():
    return {"hi": "works"}


@app.get("/authenticated-route")
def read_users_me(user: User = Depends(current_active_user)):
    return user.email
