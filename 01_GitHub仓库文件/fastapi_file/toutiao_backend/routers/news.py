from fastapi import APIRouter

#创建apirouter实例
router = APIRouter(prefix = "/api/news", tags = ["news"])

@router.get("/news")
async def get_categors():
    return {
        "message" : "获取分类成功"
    }