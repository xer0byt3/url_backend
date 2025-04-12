from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import Analytics
from typing import List
from app.users import current_active_user
from app.db import User, get_async_session
from app.crud import get_userUrls

router = APIRouter()


@router.get("/analytics",response_model=List[Analytics])
async def analytics(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    urls = await get_userUrls(session, user.id)
    if not urls:
        raise HTTPException(status_code=404, detail="No analytics found")
    return urls
