from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User
from utils.response import success_response
from utils.auth import get_current_user
from config.db_conf import get_db
from crud import favorite
from schemas.favorite import FavoriteAddRequest, FavoriteCheckResponse, FavoriteListResponse

from starlette import status

router = APIRouter(prefix="/api/favorite", tags=["favorite"])

#收藏
@router.get("/check")
async def check_favorite(
    news_id: int = Query(..., alias="newsId"), 
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    is_favorited = await favorite.is_news_favorite(db, user.id, news_id)
    return success_response(message="检查收藏状态成功", data=FavoriteCheckResponse(isFavorite=is_favorited))

@router.post("/add")
async def add_favorite(
    data: FavoriteAddRequest, 
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await favorite.add_news_favorite(db, user.id, data.news_id)
    return success_response(message="收藏成功",data = result)

#取消收藏
@router.delete("/remove")
async def remove_favorite(
    news_id: int = Query(..., alias="newsId"), 
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await favorite.remove_news_favorite(db, user.id, news_id)
    if not result: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="收藏记录不存在")
    return success_response(message="取消收藏成功")


@router.get("/list")
async def get_favorite_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, alias="pageSize", le=100,ge=1),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    rows,total = await favorite.get_favorite_list(db, user.id, page, page_size)
    favorite_list = [{
            **news.to_dict(),
            "favoriteTime": favorite_time.strftime("%Y-%m-%d %H:%M:%S"),
            "favoriteId": favorite_id
        }for news,favorite_time,favorite_id in rows]
    
    has_more = total > page_size * page
    
    data = FavoriteListResponse(list=favorite_list, total=total, has_more=has_more)
    return success_response(message="获取收藏列表成功",data = data)\
        
#清空收藏列表
@router.delete("/clear")
async def clear_favorite_list(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    count = await favorite.remove_all_favorites(db, user.id)
    return success_response(message=f"清空了{count}条数据")