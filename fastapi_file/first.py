#运行时，在终端输入 unvicorn 文件夹名.文件名:app --reload

from fastapi import FastAPI,Path,Query
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/fastapi")
async def get_hello():
    return {"message": "Hello fastapi"}

@app.get("/hello/{name}")
async def say_hello(name:str):
    return {"message":f"hello,{name}"}

@app.get("/book_id/{id}")
async def get_book_info(id: int = Path(...,gt=0,lt=101,description = "书籍范围：[0,100]")):
    return {
        "id": id,
        "title": f"这是第{id}本书"
    }

@app.get("/author/{name}")
async def get_author(name:str = Path(...,min_length = 0,max_length = 20,description = "请输入作者信息")):
    return {"message":f"这是{name}的信息"}

#需求 查询新闻 -》分页，skip：跳过的记录数，limit：返回的记录数
@app.get("/news/news_list")
async def get_news_list(
    skip : int = Query(...,description = "跳过的记录数",lt = 100), 
    limit : int = Query(10,description = "返回的记录数")
):
    return {
        "skip": skip,
        "limit": limit
    }

#需求 查询图书，包含价格和分类
@app.get("/book_info/book_list")
async def get_book_list(
    category : str = Query("Python开发", description = "图书分类", min_length = 5, max_length = 255),
    price : int = Query(..., description = "图书价格", ge = 50, le = 100)
):
    return {
        "category": f"图书分类：{category}",
        "price": f"图书价格: {price}"
    }

if __name__ == "__main__":
    uvicorn.run(app,host = "127.0.0.1",port = 8000)
