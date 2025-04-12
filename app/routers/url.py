from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas import URLRequest, URLResponse
from app.crud import create_url_mapping, get_long_url, log_click
from app.utils import generate_unique_id
from app.db import User, get_async_session
from app.users import current_active_user
from app.models import URL

router = APIRouter()


@router.post(
    "/shorten",
    response_model=URLResponse,
)
async def shorten_url(
    request: URLRequest,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
        existing_url = await db.execute(
            select(URL).filter(URL.long_url == str(request.long_url), URL.user_id == user.id)
        ) # check if the long_url is created by the user
        existing_url = existing_url.scalars().first()

        if existing_url:
            return URLResponse(url=existing_url.short_id)

        short_id = generate_unique_id(request.long_url, user.id)
        print("--->",short_id)
        while await get_long_url(db, short_id):
            short_id = generate_unique_id(request.long_url, user.id)

        await create_url_mapping(db, short_id, str(request.long_url), user.id)

        print(user.id, short_id)

        return URLResponse(url=short_id)


@router.get(
    "/{short_id}",
    response_model=URLResponse,
)
async def resolve_url(
    short_id: str, db: AsyncSession = Depends(get_async_session)
):
    url_mapping = await get_long_url(db, short_id)
    if url_mapping:
        await log_click(db, short_id)
        return URLResponse(url=url_mapping.long_url)
    else:
        raise HTTPException(status_code=404, detail="URL not found")


# allow user to delete THEIR urls:
@router.delete(
    "/{short_id}",
)
async def delete_url(
    short_id: str, db: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user)
):
    url_mapping = await db.execute(
        select(URL).filter(URL.short_id == short_id, URL.user_id == user.id)
    )
    url_mapping = url_mapping.scalars().first()
    if url_mapping:
        await db.delete(url_mapping)
        await db.commit()
        return {"message": "URL deleted"}
    else:
        raise HTTPException(status_code=404, detail="URL not found")