#中间件的运行顺序 是 代码自下而上的，start2 -> start1 -> end1 -> end2
from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.middleware("http")
async def middleware1(request,call_next):
    print("中间件1 start")
    response = await call_next(request)
    print("中间件1 end")
    return response

@app.middleware("http")
async def middleware2(request,call_next):
    print("中间件2 start")
    response = await call_next(request)
    print("中间件2 end")
    return response

@app.middleware("http")
async def middleware0(request,call_next):
    print("中间件0 start")
    response = await call_next(request)
    print("中间件0 end")
    return response

@app.get("/")
async def root():
    return {
        "message":"hello world"
    }
    
if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)