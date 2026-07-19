from fastapi import FastAPI,HTTPException
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return{
        "message" : "hello world"
    }
    
#需求：按照id查询新闻
@app.get("/news/{id}")
async def get_news(id : int):
    id_list = [1,2,3,4,5,6]
    if id not in id_list:
        raise HTTPException(status_code=404,detail="你寻找的新闻不存在")
    return{
        "id" : id
    }
    
if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)
