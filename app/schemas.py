from fastapi_users import schemas
from pydantic import BaseModel, EmailStr, Field, HttpUrl, NameEmail


class URLRequest(BaseModel):
    long_url: HttpUrl


class URLResponse(BaseModel):
    url: str


class ClickLogResponse(BaseModel):
    
    short_id: str
    long_url: HttpUrl
    count: int


class Analytics(BaseModel):
    short_id: str
    long_url: HttpUrl
    click_count: int


class UserRead(schemas.BaseUser[int]):
    pass


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr | None = Field(default=None)
    password: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserUpdate(schemas.BaseUserUpdate):
    pass
