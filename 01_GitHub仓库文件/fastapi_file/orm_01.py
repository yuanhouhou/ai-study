import os
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from datetime import datetime
from sqlalchemy import DateTime, Float, String,func, select
import uvicorn
from pydantic import BaseModel

#1.创建异步引擎

env_path = Path(__file__).resolve().parents[1] / "config" / ".env"
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("ASYNC_DATABASE_URL="):
            os.environ["ASYNC_DATABASE_URL"] = line.split("=", 1)[1].strip()

ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL", "")
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo = True,#可选，输出sql日志
    pool_size = 10,#设置连接池活跃的连接数
    max_overflow = 20#允许额外的连接数
)

#2.定义模型类 ： 基类 + 表对应的模型类
#基类 创建时间，更新时间； 书籍表： id，书名，作者，价格，出版社
class Base(DeclarativeBase):
    create_time : Mapped[datetime] = mapped_column(DateTime,insert_default=func.now(),default=func.now,comment="创建时间")
    update_time : Mapped[datetime] = mapped_column(DateTime,insert_default=func.now(),default=func.now,onupdate=func.now(),comment="更新时间")

class Book(Base):
    __tablename__ = "book"
    id : Mapped[int] = mapped_column(primary_key=True,comment="书籍ID")
    bookname : Mapped[str] = mapped_column(String(255),comment="书名")
    author : Mapped[str] = mapped_column(String(255),comment="作者")
    price : Mapped[float] = mapped_column(Float,comment="书籍价格")
    publisher : Mapped[str] = mapped_column(String(255),comment="出版社")

#3.建表 : 定义函数建表 -> fastapi 启动的时候调用建表的函数
async def create_tables():
    #获取异步引擎，创建事务 - 建表
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) # Base 模型类的元数据创建

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {
        "message" : "hello world"
    }


#需求：查询功能的接口，查询图书->依赖注入：创建依赖项获取数据库会话 + Depends 注入路由处理函数
AsyncSessionlocal = async_sessionmaker(
    bind = async_engine, # 绑定数据库引擎
    class_ = AsyncSession, # 指定会话类
    expire_on_commit = False # 提交后会话不过期，不会重新查询数据库
)

#依赖项
async def get_database():
    async with AsyncSessionlocal() as session:
        try:
            yield session # 返回数据库会话给路由处理函数
            await session.commit() # 提交事务
        except Exception:
            await session.rollback() # 有异常 回滚
            raise
        finally:
            await session.close() # 关闭会话

@app.get("/book/books")
async def get_book_list(db:AsyncSession = Depends(get_database)):
    # 查询
    result = await db.execute(select(Book))
    book = result.scalars().all()
    return book

#需求：路径参数 书籍id 
@app.get("/book/search_book_id/{book_id}")
async def get_book_list1(book_id : int,db:AsyncSession = Depends(get_database)):
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalars().first()
    return book

#需求：路径参数  价格
@app.get("/book/search_book_price/{price}")
async def get_book_list2(price : float,db:AsyncSession = Depends(get_database)):
    result = await db.execute(select(Book).where(Book.price >= price))
    book = result.scalars().all()
    return book

#需求：作者以 曹 开头的 %_
@app.get("/book/search_book_author")
async def get_book_list3(
    author : str,
    price  : float,
    db:AsyncSession = Depends(get_database)
    ):
    #like():模糊查询 %任意个字符 _单个字符 & | ~ 与或非
    result = await db.execute(select(Book).where((Book.author.like(f"{author}%")) & (Book.price >= price)))
    #result = await db.execute(select(Book).where(Book.author.like(f"{author}_"))) 只能搜出曹植,几个_就匹配几个字符
    book = result.scalars().all()
    return book

@app.get("/book/search_book_author_idlist")
async def get_book_list4(
    db:AsyncSession = Depends(get_database)
):
    #result = await db.execute(select(Book).where((Book.author.like(f"{author}%")) & (Book.price >= price)))
    #result = await db.execute(select(Book).where(Book.author.like(f"{author}_"))) 只能搜出曹植,几个_就匹配几个字符
    #需求：书籍id列表，数据库里面的id如果在 书籍id列表里面 就返回
    #id_() : 包含
    id_list = [1,3,5,7]
    result = await db.execute(select(Book).where(Book.id.in_(id_list))) 
    book = result.scalars().all()
    return book

@app.get("/book/count")
async def get_count(
    db:AsyncSession = Depends(get_database)
):
    #result = await db.execute(select(func.count(Book.id)))
    #result = await db.execute(select(func.sum(Book.price)))
    #result = await db.execute(select(func.avg(Book.price)))
    #result = await db.execute(select(func.min(Book.price)))
    result = await db.execute(select(func.max(Book.price)))
    num = result.scalar() #用来提取一个数值 -> 标量值
    return num

@app.get("/book/get_book_list")
async def get_book_list(
    page : int = 1,
    page_size : int = 3,
    db:AsyncSession = Depends(get_database)
):
    #（页码-1） * 每页数量 = 跳过的记录数
    skip = (page - 1) * page_size
    #offset: 跳过的记录数 limit: 每页的记录数
    result = await db.execute(select(Book).order_by(Book.id).offset(skip).limit(page_size))
    books = result.scalars().all()
    return books

#需求：用户输入图书信息(id,书名，作者，价格，出版社) -> 新增
#用户输入 -> 参数 -> 请求体
class BookBase(BaseModel):
    id : int
    bookname : str
    author : str
    price : float
    publisher : str
    
@app.post("/book/add_book")
async def add_book(
    book : BookBase,
    db:AsyncSession = Depends(get_database)
):
    #orm对象 -> add -> comit
    book_obj = Book(**book.__dict__)
    db.add(book_obj)
    await db.commit()
    return book

#需求：修改图书信息 先查再改
#设计思路：路径参数书籍id:作用查找 请求体参数：作用是新数据
class BookUpdate(BaseModel):
    bookname : str
    author : str
    price : float
    publisher : str

@app.put("/book/update_book/{book_id}")
async def update_book(
    book_id : int,
    data : BookUpdate,
    db:AsyncSession = Depends(get_database)
):
    #1. 查找图书
    db_book = await db.get(Book,book_id)
    
    #如果未找到，抛出异常
    if db_book is None:
        raise HTTPException(
            status_code = 404,
            detail = "查无此书"
        )
    
    #2. 重新赋值
    db_book.bookname = data.bookname
    db_book.author = data.author
    db_book.price = data.price
    db_book.publisher = data.publisher
    
    #3. 提交事务
    await db.commit()
    return db_book

#先查再删
@app.delete("/book/delete_book/{book_id}")
async def delete_book(
    book_id : int,
    db:AsyncSession = Depends(get_database)
):
    #1. 查找图书
    db_book = await db.get(Book,book_id)
    
    if db_book is None:
        raise HTTPException(
                status_code = 404,
                detail = "查无此书"
        )
    
    await db.delete(db_book)
    await db.commit()
    return {"message" : "删除成功"}    
    
if __name__ == "__main__":
    uvicorn.run("orm_01:app", host="127.0.0.1", port=8000, reload=True)
