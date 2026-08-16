import uvicorn
from fastapi import FastAPI
from routers import news
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #允许的源，开发阶段允许所有，生产环境需要指定源
    allow_credentials=True, #允许携带cookie
    allow_methods=["*"], #允许的请求方法，开发阶段允许所有，生产环境需要指定方法
    allow_headers=["*"] #允许的请求头，开发阶段允许所有，生产环境需要指定头
)


@app.get("/")
async def root():
    return {
        "message" : "hello world"
    }

# 挂载路由/注册路由
app.include_router(news.router)





if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
