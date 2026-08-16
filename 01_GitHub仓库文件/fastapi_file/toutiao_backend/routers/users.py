from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from crud import users
from schemas.users import UserAuthResponse, UserInfoResponse, UserRequest
from starlette import status
from utils.response import success_response


router = APIRouter(prefix="/api/user", tags=["users"])


@router.post("/register")
async def register(
    user_data: UserRequest,
    db: AsyncSession = Depends(get_db),
):
    # 注册逻辑 验证用户是否存在 -> 创建用户 -> 生成Token -> 响应结果
    existing_user = await users.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已存在")

    user = await users.create_user(db, user_data)
    token = await users.create_token(db, user.id)

    response_data = UserAuthResponse(
        token=token,
        user_info=UserInfoResponse.model_validate(user),
    )

    return success_response(message="注册成功", data=response_data)
