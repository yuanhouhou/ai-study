from fastapi import FastAPI,Query,Depends

app = FastAPI()

@app.get("/")
async def root():
    return {
        "message":"hello world"
    }

# 分页参数逻辑共用 ： 新闻列表和用户列表
async def common_parameters(
    skip : int = Query(default=0,ge=0),
    limit : int = Query(default=10,le=60)
):
    return {
        "skip" : skip,
        "limit" : limit
    }



# @app.get("/news/news_list")
# async def get_news_list():
#     return {
#         "message":"hello world"
#     }

@app.get("/news/news_list")
async def get_news_list(commons = Depends(common_parameters)):
    return commons

# @app.get("/user/user_list")
# async def get_user_list():
#     return {
#         "message":"hello world"
#     }

@app.get("/user/user_list")
async def get_user_list(commons = Depends(common_parameters)):
    return  commons