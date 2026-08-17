from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from models.favorite import Favorite


async def is_news_favorite(
    db: AsyncSession,
    user_id : int,
    news_id : int
):
    query = select(Favorite).where(
        Favorite.user_id == user_id,
        Favorite.news_id == news_id
        )
    result = await db.execute(query)
    #是否有收藏记录
    return result.scalar_one_or_none() is not None

async def add_news_favorite(
    db: AsyncSession,
    user_id : int,
    news_id : int
):
    favorite = Favorite(user_id=user_id, news_id=news_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite

async def remove_news_favorite(
    db: AsyncSession,
    user_id : int,
    news_id : int
):
    stmt = delete(Favorite).where(
        Favorite.user_id == user_id,
        Favorite.news_id == news_id
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0 