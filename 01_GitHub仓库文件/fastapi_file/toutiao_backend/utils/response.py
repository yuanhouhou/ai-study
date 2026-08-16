from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


def success_response(
    message: str = "success",
    data=None
):
    content = {
        "code": 200,
        "message": message,
        "data": data,
    }
    # 目标：把 FastAPI、Pydantic、ORM 对象都统一响应为 code、message、data
    return JSONResponse(content=jsonable_encoder(content))
