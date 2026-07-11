#fastapi的后端框架，在调试的时候有两种方式检查同步异步
#1.在网页端的url后缀加上/sync或者/async，等待返回值
#2.在网页端的url后缀加入docs进入互动式的调试窗口
import asyncio
import time
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/sync")
def func_sync():
    start = time.time()
    for _ in range(10):
        time.sleep(1)
    end = time.time()
    return {"time": f"{end - start:.2f}s"}


@app.get("/")
def index():
    return "你好，这是sync和async的测试接口页面"


@app.get("/async")
async def func_async():
    start = time.time()
    tasks = [asyncio.sleep(1) for _ in range(10)]
    await asyncio.gather(*tasks)
    end = time.time()
    return {"time": f"{end - start:.2f}s"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
