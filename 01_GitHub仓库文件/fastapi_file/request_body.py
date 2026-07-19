from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel,Field
import uvicorn
#Field：限制请求体里的字段
#basemodel 定义了一个请求体的数据格式
app = FastAPI()

@app.get("/")
async def root():
    return {
        "message": "hello world"
    }
    
#注册 用户名和密码
class User(BaseModel):
    username : str = Field(default = "张三",min_length=2,max_length=10,description = "用户名长度要求2-10字")
    password : str = Field(...,min_length = 8,max_length = 16,description="密码不低于8位，不多于16位")

#get 一般是请求查询，post 是提交数据
@app.post("/register")
async def register(user:User):
    return user

#需求：新增图书，包含作者，书名，出版社，售价
class Add_book(BaseModel):
    book_name : str = Field(...,min_length=2,max_length=20,description="书名：不能为空，长度2-20")
    author_name : str = Field(...,min_length=2,max_length=10,description="作者名：长度2-10")
    publishing_company : str = Field(default="黑马出版社",description="出版社：默认黑马出版社")
    price : int = Field(...,gt=0,description="价格：不能为空，大于0元")
    
@app.post("/book_add")
async def Add_new_book(book:Add_book):
    return book

#接口 -> 在装饰器中响应html代码 
@app.get("/html",response_class=HTMLResponse)
async def get_html():
    return "<h1>这是1级标题<h1>"

#接口 -> 返回一张图片,流媒体，音视频
@app.get("/image", response_class=FileResponse)
async def get_file():
    path = r"E:\vscode_project\python_study\deeplearning_file\study_resourece\pytorch-tutorial-main\pytorch-tutorial-main\imgs\weixin.jpg"
    return FileResponse(path)

#需求：新闻接口 -> 响应数据格式 id title content
#自定义响应，要保持return和请求体的数据格式保持一致
class News(BaseModel):
    id : int
    title : str
    content : str

@app.get("/news/{id}",response_model=News)
async def get_news(id : int):
    return {
        "id" : id,
        "title" : f"这是第{id}个新闻",
        "content" : "这是新闻内容"
    }


if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)
