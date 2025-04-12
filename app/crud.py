import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import URL, ClickLog
from sqlalchemy import func

# ✅
async def create_url_mapping(
    db: AsyncSession, short_id: str, long_url: str, user_id: int
):
    """
    saves the short_id and long_url.
    """
    db_url_mapping = URL(short_id=short_id, long_url=long_url, user_id=user_id)
    db.add(db_url_mapping)
    await db.commit()
    await db.refresh(db_url_mapping)
    return db_url_mapping

# ✅
async def get_long_url(db: AsyncSession, short_id: str):
    result = await db.execute(select(URL).filter(URL.short_id == short_id))
    return result.scalars().first()  # Retrieve the first result from the async query

# ✅
async def log_click(db: AsyncSession, short_id: str):
    click_log = ClickLog(short_id=short_id, clicked_at=datetime.datetime.now())
    db.add(click_log)
    await db.commit()
    await db.refresh(click_log)
    return click_log

import pprint

async def get_userUrls(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(URL.short_id, URL.long_url, func.count(ClickLog.id).label("click_count"))
        .outerjoin(ClickLog, URL.short_id == ClickLog.short_id)
        .where(URL.user_id == user_id)
        .group_by(URL.short_id, URL.long_url)
    )
    print("user id is:", user_id)
    urls_with_clicks = result.fetchall()
    pprint.pprint(urls_with_clicks)
    pprint.pprint(urls_with_clicks[0])
    pprint.pprint(urls_with_clicks[0].short_id)
    pprint.pprint(urls_with_clicks[0].long_url)
    pprint.pprint(urls_with_clicks[0].click_count)
    
    
    return [
        {
            "short_id": row.short_id,
            "long_url": row.long_url,
            "click_count": row.click_count,
        }
        for row in urls_with_clicks
    ]
