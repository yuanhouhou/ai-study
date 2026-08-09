import uvicorn
from fastapi import FastAPI
from routers import news


app = FastAPI()


@app.get("/")
async def root():
    return {
        "message" : "hello world"
    }

# 挂载路由/注册路由
app.include_router(news.router)





if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
