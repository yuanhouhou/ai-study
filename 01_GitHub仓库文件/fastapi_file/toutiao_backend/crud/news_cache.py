from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category, News
from cache.news_cache import get_cached_categories, set_cache_categories,get_cache_news_list,set_cache_news_list
from schemas.base import NewsItemBase

async def get_categories(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100
):
    #先尝试从缓存中获取数据
    cached_categories = await get_cached_categories()
    if cached_categories:
        return cached_categories

    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all() # ORM数据

    #写入缓存
    if categories:
        categories = jsonable_encoder(categories)
        await set_cache_categories(categories)

    #返回数据
    return categories



async def get_news_list(
    db: AsyncSession,
    category_id: int,
    skip: int = 0,
    limit: int = 10
):
    #尝试从缓存获取数据列表
    #跳过的数量skip = (页码 - 1 ) * 每页数量 -> 页码 = (skip + limit) / limit
    #get_cache_news_list(分类id,页码,每页数量)
    page = skip // limit + 1
    cached_list = await get_cache_news_list(category_id,page,limit) #缓存数据 json
    if cached_list:
        #return cached_list 这是json
        return [News(**item)for item in cached_list]

    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    news_list =  result.scalars().all()
    #写入缓存
    if news_list:
        #先把orm 转换为 字典才能写入缓存
        #orm 转换为 pydantic 再转字典
        #by_alias = False 不适用别名 保存pythjon风格 因为redis数据是给后端用的
        news_data = [NewsItemBase.model_validate(item).model_dump(mode = "json",by_alias = False) for item in news_list]
        await set_cache_news_list(category_id,page,limit,news_data)
    return news_list


async def get_news_count(
    db: AsyncSession,
    category_id: int
):
    # 查询指定分类下的新闻数量
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one() # 返回一个数字，只会有一个查询结果


# 响应结果：当前新闻详情 + 增加 1 次浏览量 + 相关新闻
async def get_news_detail(
    db: AsyncSession,
    news_id: int
):
    # 获取新闻详情
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

#增加浏览量
async def increase_news_view_count(
    db: AsyncSession,
    news_id: int
):
    stmt = (
        update(News)
        .where(News.id == news_id)
        .values(views = News.views + 1)
    )
    result = await db.execute(stmt)
    await db.commit()

    # 数据库的更新操作 -> 检查数据库是否真的命中了数据 -> 命中了返回True
    return result.rowcount > 0

# 获取相关新闻
async def get_related_news(
    db: AsyncSession,
    news_id: int,
    category_id: int,
    limit: int = 5
):
    #order_by 排序 -> 浏览量和发布时间
    stmt = select(News).where(
        News.id != news_id,
        News.category_id == category_id
    ).order_by(
        News.views.desc(), #默认是升序，desc是降序
        News.publish_time.desc()
    ).limit(limit)

    result = await db.execute(stmt)
    #return result.scalars().all()
    related_news = result.scalars().all()

    # 列表推导式 推导出新闻的核心数据，然后再return

    return [{
        "id" : news_detail.id,
        "title" : news_detail.title,
        "content" : news_detail.content,
        "image" : news_detail.image,
        "author" : news_detail.author,
        "publishTime" : news_detail.publish_time.strftime("%Y-%m-%d %H:%M:%S"),
        "categoryId" : news_detail.category_id,
        "views" : news_detail.views,
        } for news_detail in related_news]
