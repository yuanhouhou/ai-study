# FastAPI 学习记录

这个文件夹用于记录 FastAPI 的基础用法示例，当前主要包含：

- `first.py`：路由、路径参数、查询参数示例
- `sync_async.py`：同步接口和异步接口耗时对比示例
- `middleware.py`：中间件的定义和多个中间件的执行顺序示例
- `depends.py`：依赖注入系统示例，复用分页查询参数逻辑
- `orm_01.py`：SQLAlchemy 异步 ORM 示例，包含建表、查询、分页、新增、更新、删除
- `toutiao_backend/`：模块化路由示例，把业务接口拆分到 `routers/` 后再挂载到主应用

README 分工：

- 本文件：作为 FastAPI 学习和知识总结 README，记录概念、示例、常见写法和学习路线。
- `toutiao_backend/README.md`：作为项目实操 README，记录新闻后端项目的功能、数据库、接口、运行方式和实操经验。

## 目录

- [怎么运行 FastAPI 项目](#怎么运行-fastapi-项目)
- [怎么访问交互式文档](#怎么访问交互式文档)
- [路由是什么](#路由是什么)
- [模块化路由](#模块化路由)
  - [接口实现流程](#接口实现流程)
  - [学习 README 和项目 README 的分工](#学习-readme-和项目-readme-的分工)
- [参数的作用](#参数的作用)
- [参数分类](#参数分类)
- [路径参数](#路径参数)
- [查询参数](#查询参数)
- [同步和异步接口耗时对比](#同步和异步接口耗时对比)
- [请求体参数](#请求体参数)
- [请求体字段校验](#请求体字段校验)
- [响应类型](#响应类型)
- [响应数据模型](#响应数据模型)
- [用户注册和 Token](#用户注册和-token)
- [登录态依赖和用户行为接口](#登录态依赖和用户行为接口)
- [异常处理](#异常处理)
- [中间件](#中间件)
- [依赖注入](#依赖注入)
- [Redis 缓存](#redis-缓存)
- [ORM 简介](#orm-简介)
- [SQLAlchemy 2.x 常用导入](#sqlalchemy-2x-常用导入)
- [SQLAlchemy 异步 ORM 建表示例](#sqlalchemy-异步-orm-建表示例)
  - [连接串来源](#连接串来源)
  - [异步引擎和会话](#异步引擎和会话)
  - [模型定义和启动建表](#模型定义和启动建表)
  - [启动命令](#启动命令)
  - [查询全部数据](#查询全部数据)
  - [条件查询](#条件查询)
  - [模糊查询和逻辑条件](#模糊查询和逻辑条件)
  - [聚合查询](#聚合查询)
  - [分页查询](#分页查询)
  - [新增数据](#新增数据)
  - [更新数据](#更新数据)
  - [删除数据](#删除数据)
  - [ORM 查询总结](#orm-查询总结)

## 怎么运行 FastAPI 项目

推荐在项目根目录运行：

```powershell
uvicorn fastapi_file.first:app --reload
```

如果要运行同步/异步耗时对比示例：

```powershell
uvicorn fastapi_file.sync_async:app --reload
```

如果要运行中间件示例：

```powershell
uvicorn fastapi_file.middleware:app --reload
```

如果要运行依赖注入示例：

```powershell
uvicorn fastapi_file.depends:app --reload
```

如果要运行 SQLAlchemy 异步 ORM 示例：

```powershell
uvicorn fastapi_file.orm_01:app --reload --app-dir ".\01_GitHub仓库文件"
```

如果已经先进入 `01_GitHub仓库文件` 目录，则可以继续使用：

```powershell
uvicorn fastapi_file.orm_01:app --reload
```

如果要运行模块化路由示例：

```powershell
cd .\01_GitHub仓库文件\fastapi_file\toutiao_backend
python -m uvicorn main:app --reload
```

其中：

- `fastapi_file.first` 表示 `fastapi_file/first.py`
- `app` 表示代码里的 `app = FastAPI()`
- `--reload` 表示修改代码并保存后，服务会自动重启

也可以直接运行 Python 文件：

```powershell
python fastapi_file\first.py
```

但是直接运行没有 `--reload` 热更新效果，修改代码后需要手动停止并重新运行。

## 怎么访问交互式文档

服务启动后，浏览器访问：

```text
http://127.0.0.1:8000/docs
```

这个页面是 FastAPI 自动生成的交互式接口文档，可以直接测试接口参数和返回结果。

也可以访问：

```text
http://127.0.0.1:8000/redoc
```

## 路由是什么

路由就是 URL 地址和处理函数之间的映射关系。

当用户访问某个 URL 时，服务器会根据路由找到对应的 Python 函数，执行函数并返回结果。

例如：

```python
@app.get("/")
async def root():
    return {"message": "Hello World"}
```

这段代码表示：

- `app`：FastAPI 应用实例
- `get`：请求方法是 GET
- `/`：请求路径是根路径
- `root`：处理这个请求的函数
- `return`：返回给客户端的数据

访问：

```text
http://127.0.0.1:8000/
```

返回：

```json
{"message": "Hello World"}
```

FastAPI 的路由定义基于 Python 的装饰器模式：

```python
@app.get("/fastapi")
async def get_hello():
    return {"message": "Hello fastapi"}
```

这里的 `@app.get("/fastapi")` 就是把 URL `/fastapi` 和函数 `get_hello` 绑定起来。

## 模块化路由

当项目变大以后，如果所有接口都写在 `main.py` 里，文件会越来越长，业务代码也容易混在一起。模块化路由就是把每个业务功能的接口拆分到独立文件里，再统一挂载到主应用中。

模块化路由的好处：

- 项目结构更清晰：不同业务接口放到不同文件，不会全部堆在 `main.py`
- 更容易维护：每个模块只负责自己的接口，查找和修改更方便
- 避免 `main.py` 爆炸：`main.py` 主要负责创建应用、挂载路由和启动服务

当前 `toutiao_backend` 示例目录：

```text
toutiao_backend/
├── main.py
└── routers/
    └── news.py
```

### 编写独立路由模块

在 `routers/news.py` 中先创建 `APIRouter` 实例：

```python
from fastapi import APIRouter

# 创建 APIRouter 实例
router = APIRouter(prefix="/api/news", tags=["news"])

@router.get("/news")
async def get_categors():
    return {
        "message": "获取分类成功"
    }
```

这里的关键点：

- `APIRouter`：创建一个独立路由模块
- `prefix="/api/news"`：给这个模块下所有接口统一添加路径前缀
- `tags=["news"]`：在 `/docs` 文档中把接口归到 `news` 分组
- `@router.get("/news")`：这里用的是 `router`，不是 `app`

最终访问路径由 `prefix` 和接口路径拼接得到：

```text
/api/news + /news = /api/news/news
```

在当前 `toutiao_backend` 项目中，分类接口已经改成更语义化的：

```python
@router.get("/categories")
```

所以实际分类接口路径是：

```text
/api/news/categories
```

### 在 main.py 中挂载路由

在 `main.py` 中导入路由模块，并通过 `include_router()` 注册到主应用：

```python
from fastapi import FastAPI
from routers import news

app = FastAPI()

@app.get("/")
async def root():
    return {
        "message": "hello world"
    }

# 挂载路由/注册路由
app.include_router(news.router)
```

这里的核心是：

```python
app.include_router(news.router)
```

它的意思是：把 `routers/news.py` 里定义好的 `router` 挂载到当前 FastAPI 主应用里。

如果出现：

```text
AttributeError: module 'routers.news' has no attribute 'router'
```

通常表示 `routers/news.py` 中没有定义下面这个变量，或者保存到了别的文件：

```python
router = APIRouter(...)
```

### 运行和访问

启动模块化路由示例：

```powershell
cd .\01_GitHub仓库文件\fastapi_file\toutiao_backend
python -m uvicorn main:app --reload
```

访问根路径：

```text
http://127.0.0.1:8000/
```

访问新闻模块接口：

```text
http://127.0.0.1:8000/api/news/categories
```

在 `/docs` 中也可以看到 `news` 分组下的接口。

### 接口实现流程

项目实操中，一个连接数据库的接口通常可以按下面的顺序实现：

```text
模块化路由 -> 定义模型类 -> 数据库 CRUD -> 路由调用逻辑
```

对应到 `toutiao_backend`：

| 步骤 | 位置 | 作用 |
| --- | --- | --- |
| 模块化路由 | `routers/news.py` | 使用 `APIRouter` 定义接口路径、分组和请求参数 |
| 定义模型类 | `models/news.py` | 使用 SQLAlchemy ORM 类映射数据库表 |
| 数据库 CRUD | `crud/news.py` | 封装 `select()`、`add()`、`update()`、`delete()` 等数据库操作 |
| 路由调用逻辑 | `routers/news.py` | 使用 `Depends` 注入数据库会话，调用 CRUD 并返回结果 |

以新闻分类列表为例：

```text
GET /api/news/categories
-> routers/news.py 接收 skip、limit
-> Depends(get_db) 提供 AsyncSession
-> crud/news.py 执行 select(Category)
-> models/news.py 映射 news_category 表
-> 返回分类列表
```

这样拆分后，路由层负责接口，CRUD 层负责数据库操作，模型层负责表结构映射，代码边界更清楚。

### 学习 README 和项目 README 的分工

学习阶段建议把 README 分成两类：

| README | 定位 | 主要内容 |
| --- | --- | --- |
| `fastapi_file/README.md` | 学习和知识总结 | FastAPI 概念、语法、示例、常见问题 |
| `toutiao_backend/README.md` | 项目实操记录 | 项目功能、数据库、接口、运行方式、实操复盘 |

这样做的好处是：学习笔记可以持续沉淀通用知识，项目 README 可以聚焦项目本身，不会把概念教程和项目说明混在一起。

## 参数的作用

参数是客户端发送请求时附带的额外信息。

参数的作用是让同一个接口可以根据不同输入返回不同输出，实现动态交互。

例如：

```python
@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"hello,{name}"}
```

访问：

```text
http://127.0.0.1:8000/hello/yuan
```

返回：

```json
{"message": "hello,yuan"}
```

## 参数分类

FastAPI 常见参数可以分为三类：

| 类型 | 位置 | 作用 | 常用方法 |
| --- | --- | --- | --- |
| 路径参数 | URL 路径的一部分 | 指向唯一、特定的资源 | GET |
| 查询参数 | URL 的 `?` 后面 | 过滤、排序、分页等 | GET |
| 请求体 | HTTP 请求的 body 中 | 创建、更新资源，传递复杂数据 | POST、PUT |

## 路径参数

路径参数写在 URL 路径中，用 `{}` 表示。

当前代码示例：

```python
@app.get("/book_id/{id}")
async def get_book_info(
    id: int = Path(..., gt=0, lt=101, description="书籍范围：[0,100]")
):
    return {
        "id": id,
        "title": f"这是第{id}本书"
    }
```

访问：

```text
http://127.0.0.1:8000/book_id/2
```

返回第 2 本书的信息。

这里的参数限制是：

- `id` 必须是整数
- `gt=0` 表示大于 0
- `lt=101` 表示小于 101

所以允许的范围是 `1 ~ 100`。

另一个路径参数示例：

```python
@app.get("/author/{name}")
async def get_author(
    name: str = Path(..., min_length=0, max_length=20, description="请输入作者信息")
):
    return {"message": f"这是{name}的信息"}
```

## 查询参数

查询参数写在 URL 的 `?` 后面。

例如分页查询新闻：

```python
@app.get("/news/news_list")
async def get_news_list(
    skip: int = Query(..., description="跳过的记录数", lt=100),
    limit: int = Query(10, description="返回的记录数")
):
    return {
        "skip": skip,
        "limit": limit
    }
```

访问：

```text
http://127.0.0.1:8000/news/news_list?skip=0&limit=10
```

含义：

- `skip=0`：跳过 0 条记录
- `limit=10`：返回 10 条记录

查询图书示例：

```python
@app.get("/book_info/book_list")
async def get_book_list(
    category: str = Query("Python开发", description="图书分类", min_length=5, max_length=255),
    price: int = Query(..., description="图书价格", ge=50, le=100)
):
    return {
        "category": f"图书分类：{category}",
        "price": f"图书价格: {price}"
    }
```

访问：

```text
http://127.0.0.1:8000/book_info/book_list?category=Python开发&price=80
```

参数要求：

- `category`：图书分类，默认值是 `Python开发`，长度限制 `5 ~ 255`
- `price`：图书价格，范围限制 `50 ~ 100`

### 查询参数别名 alias

当前 `toutiao_backend` 项目里，前端参数通常使用小驼峰或简短名称，例如：

```text
/api/news/list?categoryId=1&page=1&pageSize=10
/api/news/detail?id=2
```

Python 变量名更适合写成下划线风格，所以可以用 `Query(..., alias="前端参数名")` 做映射：

```python
@router.get("/list")
async def get_news_detail(
    category_id: int = Query(..., alias="categoryId"),
    page_size: int = Query(10, alias="pageSize")
):
    ...
```

这里客户端传 `categoryId`，函数内部使用 `category_id`。

详情接口同理：

```python
@router.get("/detail")
async def get_news_list(
    news_id: int = Query(..., alias="id")
):
    ...
```

注意：Swagger 会把函数签名里每一个 `Query` 参数都显示出来。如果为了兼容大小写同时写 `id` 和 `Id` 两个参数，文档页面就会出现两个输入框。项目里统一使用小写 `id` 后，只需要保留一个参数。

## 同步和异步接口耗时对比

`sync_async.py` 中有两个接口：

```text
/sync
/async
```

同步接口：

```python
@app.get("/sync")
def func_sync():
    start = time.time()
    for _ in range(10):
        time.sleep(1)
    end = time.time()
    return {"time": f"{end - start:.2f}s"}
```

它会连续执行 10 次 `time.sleep(1)`，所以耗时大约 10 秒。

异步接口：

```python
@app.get("/async")
async def func_async():
    start = time.time()
    tasks = [asyncio.sleep(1) for _ in range(10)]
    await asyncio.gather(*tasks)
    end = time.time()
    return {"time": f"{end - start:.2f}s"}
```

它会同时等待 10 个 `asyncio.sleep(1)`，所以耗时大约 1 秒。

启动：

```powershell
uvicorn fastapi_file.sync_async:app --reload
```

访问：

```text
http://127.0.0.1:8000/sync
http://127.0.0.1:8000/async
```

## 请求体参数

请求体英文是 `Request Body`。

在 HTTP 请求中，一个完整请求通常由三部分组成：

- 请求行：包含请求方法、URL、协议版本
- 请求头：包含元数据信息，例如 `Content-Type`、`Authorization`
- 请求体：实际要发送的数据内容

请求体位于 HTTP 请求的消息体 `body` 中，常用于创建、更新资源，携带较复杂的数据，例如 JSON。

在 FastAPI 中，请求体通常配合 `POST`、`PUT` 等方法使用。

例如 `request_body.py` 中的注册接口：

```python
from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

@app.post("/register")
async def register(user: User):
    return user
```

这里的 `User` 定义了请求体的数据格式。

测试时可以发送：

```json
{
  "username": "张三",
  "password": "12345678"
}
```

`@app.post("/register")` 表示这个接口使用 `POST` 请求。一般来说：

- `GET`：用于查询数据
- `POST`：用于提交或新增数据

新增图书示例：

```python
class Add_book(BaseModel):
    book_name: str
    author_name: str
    publishing_company: str
    price: int

@app.post("/book_add")
async def Add_new_book(book: Add_book):
    return book
```

测试请求体：

```json
{
  "book_name": "Python入门",
  "author_name": "张三",
  "publishing_company": "黑马出版社",
  "price": 88
}
```

当前代码只是接收并返回请求体内容，不会永久保存数据。

## 请求体字段校验

请求体参数可以通过两种方式添加类型和校验：

- Python 原生类型注解，例如 `str`、`int`
- Pydantic 的 `Field` 注解

例如：

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    username: str = Field(
        default="张三",
        min_length=2,
        max_length=10,
        description="用户名长度要求2-10字"
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=16,
        description="密码不低于8位，不多于16位"
    )
```

这里：

- `default="张三"`：默认值是张三
- `...`：表示这个字段必填
- `min_length`：最小长度
- `max_length`：最大长度
- `description`：在 `/docs` 文档中显示的说明

新增图书字段校验示例：

```python
class Add_book(BaseModel):
    book_name: str = Field(..., min_length=2, max_length=20, description="书名：不能为空，长度2-20")
    author_name: str = Field(..., min_length=2, max_length=10, description="作者名：长度2-10")
    publishing_company: str = Field(default="黑马出版社", description="出版社：默认黑马出版社")
    price: int = Field(..., gt=0, description="价格：不能为空，大于0元")
```

`Field` 主要用于请求体字段；前面学过的 `Path` 用于路径参数，`Query` 用于查询参数。

## 响应类型

默认情况下，FastAPI 会把路径操作函数返回的 Python 对象，例如字典、列表、Pydantic 模型，自动转换为 JSON 格式返回。

例如：

```python
@app.get("/")
async def root():
    return {"message": "hello world"}
```

默认返回 JSON。

如果需要返回非 JSON 数据，例如 HTML、文件、图片、流式数据或重定向，可以使用 FastAPI 提供的响应类型。

常见响应类型：

| 响应类型 | 用途 | 示例 |
| --- | --- | --- |
| JSONResponse | 默认响应，返回 JSON 数据 | `return {"key": "value"}` |
| HTMLResponse | 返回 HTML 内容 | `return "<h1>标题</h1>"` |
| PlainTextResponse | 返回纯文本 | `return "text"` |
| FileResponse | 返回文件或图片 | `return FileResponse(path)` |
| StreamingResponse | 流式响应 | 生成器函数返回数据 |
| RedirectResponse | 重定向 | `return RedirectResponse(url)` |

`request_body.py` 中的 HTML 示例：

```python
from fastapi.responses import HTMLResponse

@app.get("/html", response_class=HTMLResponse)
async def get_html():
    return "<h1>这是1级标题<h1>"
```

这里在装饰器中指定 `response_class=HTMLResponse`，适合固定返回类型的场景。

文件或图片响应示例：

```python
from fastapi.responses import FileResponse

@app.get("/image", response_class=FileResponse)
async def get_file():
    path = r"E:\vscode_project\python_study\deeplearning_file\study_resourece\pytorch-tutorial-main\pytorch-tutorial-main\imgs\weixin.jpg"
    return FileResponse(path)
```

这里返回的是一个文件响应对象，适合文件下载、图片返回等场景。

## 响应数据模型

如果想规定接口返回的数据格式，应使用 `response_model`。

`response_model` 用的是 Pydantic 模型，不是 `response_class`。

例如新闻接口：

```python
class News(BaseModel):
    id: int
    title: str
    content: str

@app.get("/news/{id}", response_model=News)
async def get_news(id: int):
    return {
        "id": id,
        "title": f"这是第{id}个新闻",
        "content": "这是新闻内容"
    }
```

这里：

- `response_model=News`：约束返回数据必须符合 `News` 的结构
- `response_class=HTMLResponse`：控制响应类型，比如 HTML、文件等

简单区分：

```text
response_model：控制返回数据格式
response_class：控制响应内容类型
```

## 用户注册和 Token

当前 `toutiao_backend` 项目实现了用户注册接口：

```text
POST /api/user/register
```

请求体使用 Pydantic 模型接收：

```python
class UserRequest(BaseModel):
    username: str
    password: str
```

注册接口的核心流程可以拆成：

```text
进入请求 -> 根据 username 查询用户 -> 不存在则创建用户 -> 生成 Token -> 返回响应结果
```

其中用户名查询使用：

```python
query = select(User).where(User.username == username)
result = await db.execute(query)
return result.scalar_one_or_none()
```

创建用户时先加密密码，再写入数据库：

```python
hashed_password = security.get_hash_password(user_data.password)
user = User(username=user_data.username, password=hashed_password)
db.add(user)
await db.commit()
await db.refresh(user)
```

Token 是服务器发给客户端的一段字符串，用来让客户端在后续请求中证明“我已经登录过”。当前项目使用 `uuid.uuid4()` 生成临时 Token：

```python
token = str(uuid.uuid4())
expires_at = datetime.now() + timedelta(days=7)
```

如果用户已经有 Token，就更新原来的 Token；如果没有，就新增一条 `user_token` 记录。更新和新增后都要 `commit()`，否则数据不会真正保存到数据库。

### 密码加密

当前项目使用 `bcrypt` 加密密码：

```python
password_bytes = password.encode("utf-8")
hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
return hashed_password.decode("utf-8")
```

bcrypt 对原始密码有 72 bytes 限制。这里是字节数，不是字符数。英文数字通常一个字符 1 byte，中文通常一个字符 3 bytes。

如果使用 `passlib + bcrypt` 时短密码也误报：

```text
ValueError: password cannot be longer than 72 bytes
```

可能是依赖版本兼容问题。当前项目绕开 `passlib`，直接使用 `bcrypt.hashpw()`。

### 统一响应结构

为了让前端处理接口更稳定，可以统一返回：

```json
{
  "code": 200,
  "message": "注册成功",
  "data": {}
}
```

当前项目封装了：

```python
def success_response(message: str = "success", data=None):
    content = {
        "code": 200,
        "message": message,
        "data": data,
    }
    return JSONResponse(content=jsonable_encoder(content))
```

`jsonable_encoder()` 可以把 Pydantic 模型、ORM 对象等转换成 JSON 可以序列化的数据。

注册接口返回数据使用 Pydantic 响应模型组织：

```python
class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(..., alias="userInfo")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )
```

这里的 `alias="userInfo"` 表示 Python 内部字段叫 `user_info`，但返回给前端时使用 `userInfo`。

## 登录态依赖和用户行为接口

注册和登录接口返回 Token 后，前端可以在后续请求中通过请求头携带 Token：

```text
Authorization: uuid生成的访问令牌
```

后端可以把“解析 Token -> 查询用户 -> 判断是否有效”封装成依赖项：

```python
async def get_current_user(
    authorization: Optional[str] = Header(None, alias="Authorization"),
    db: AsyncSession = Depends(get_db)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="未登录")

    token = authorization.replace("Bearer ", "")
    user = await users.get_user_by_token(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="无效令牌或已过期的令牌")

    return user
```

需要登录态的接口只要写：

```python
user: User = Depends(get_current_user)
```

这样路由函数就能直接拿到当前用户，不需要每个接口重复写 Token 校验逻辑。

用户行为类接口，例如收藏、浏览历史、个人资料修改，通常都需要同时满足两个条件：

- 请求中带有有效 Token，能确定当前用户是谁。
- 数据操作必须带上 `user_id` 条件，避免修改或删除其他用户的数据。

收藏接口的常见流程：

```text
检查收藏：按 user_id + news_id 查询 favorite 表
添加收藏：写入 user_id + news_id
取消收藏：按 user_id + news_id 删除，并用 rowcount 判断是否真的删除成功
```

前端字段名和 Python 字段名不一致时，可以用 Pydantic 的 `alias`：

```python
class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")
```

这样前端传 `newsId`，后端代码里仍然使用更符合 Python 风格的 `news_id`。

浏览历史通常不是每次浏览都插入新记录。先按 `user_id + news_id` 查询：已有记录则更新时间，没有记录才新增；查询列表时再按 `view_time` 倒序分页。这样同一用户反复阅读同一篇新闻，列表中只保留一条最新记录。

新闻、收藏和浏览历史列表需要共享相同新闻字段时，可以把公共字段抽到基础 Pydantic 模型中。字段类型应保持与 ORM 数据一致，例如数据库中的 `publish_time` 是 `datetime`，响应模型也使用 `datetime`，再通过 `alias="publishTime"` 输出为前端需要的小驼峰字段名。

## 异常处理

当客户端请求的数据不合法，或者资源不存在时，可以使用 `HTTPException` 主动中断请求并返回错误响应。

例如 `fastapi_exception.py` 中按照 id 查询新闻：

```python
from fastapi import FastAPI, HTTPException

@app.get("/news/{id}")
async def get_news(id: int):
    id_list = [1, 2, 3, 4, 5, 6]
    if id not in id_list:
        raise HTTPException(status_code=404, detail="你寻找的新闻不存在")
    return {
        "id": id
    }
```

访问存在的新闻：

```text
http://127.0.0.1:8000/news/1
```

返回：

```json
{"id": 1}
```

访问不存在的新闻：

```text
http://127.0.0.1:8000/news/100
```

返回 404 错误：

```json
{
  "detail": "你寻找的新闻不存在"
}
```

常见状态码：

- `400`：请求参数错误
- `401`：未认证
- `403`：没有权限
- `404`：资源不存在
- `500`：服务器内部错误

异常处理适合处理客户端引发的错误，例如资源找不到、认证失败、参数不合法等。

## 中间件

中间件英文是 `Middleware`，它是在每个请求进入 FastAPI 应用时都会执行的函数。

可以把中间件理解为请求和路由处理函数之间的一层统一处理逻辑：

```text
客户端请求 -> 中间件 -> 路由处理函数 -> 中间件 -> 客户端响应
```

它会在请求真正到达路径操作函数之前执行一次，也会在响应返回给客户端之前再执行一次。

中间件适合处理多个接口都需要的公共逻辑，例如：

- 身份认证
- 日志记录
- 跨域处理
- 响应头处理
- 性能监控

在 FastAPI 中，定义中间件需要在函数顶部使用装饰器：

```python
@app.middleware("http")
async def middleware(request, call_next):
    print("中间件开始处理 -- start")
    response = await call_next(request)
    print("中间件处理完成 -- end")
    return response
```

这里有两个关键参数：

- `request`：当前请求对象
- `call_next`：把请求继续传递给后面的中间件或路由处理函数

`await call_next(request)` 之前的代码，会在请求到达接口函数之前执行；后面的代码，会在接口函数返回响应之后执行。

当前 `middleware.py` 中定义了 3 个中间件：

```python
@app.middleware("http")
async def middleware1(request, call_next):
    print("中间件1 start")
    response = await call_next(request)
    print("中间件1 end")
    return response

@app.middleware("http")
async def middleware2(request, call_next):
    print("中间件2 start")
    response = await call_next(request)
    print("中间件2 end")
    return response

@app.middleware("http")
async def middleware0(request, call_next):
    print("中间件0 start")
    response = await call_next(request)
    print("中间件0 end")
    return response
```

多个中间件的执行顺序是：请求进入时自下而上，响应返回时再反向回来。

按照当前代码，访问 `/` 时大致输出顺序是：

```text
中间件0 start
中间件2 start
中间件1 start
中间件1 end
中间件2 end
中间件0 end
```

启动示例：

```powershell
uvicorn fastapi_file.middleware:app --reload
```

访问：

```text
http://127.0.0.1:8000/
```

## 依赖注入

依赖注入可以用来共享通用逻辑，避免在多个接口中重复写相同代码。

图片里的核心思路是：

```text
创建依赖项 -> 导入 Depends -> 声明依赖项
```

依赖项可以是一个可复用的函数或类，负责提供某种功能或数据。FastAPI 会自动调用依赖项，并把结果注入到路径操作函数中。

依赖注入常见应用场景：

| 场景 | 作用 |
| --- | --- |
| 处理请求参数 | 从请求中提取并校验路径参数、查询参数、请求体 |
| 共享业务逻辑 | 抽取多个路由公用的代码 |
| 共享数据库连接 | 管理数据库会话的创建、使用、关闭 |
| 安全和认证 | 验证用户身份、检查权限和角色要求 |

当前 `depends.py` 中把分页参数抽成了一个公共依赖：

```python
from fastapi import FastAPI, Query, Depends

app = FastAPI()

async def common_parameters(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, le=60)
):
    return {
        "skip": skip,
        "limit": limit
    }
```

这里的 `common_parameters` 就是依赖项，它负责统一处理分页参数：

- `skip`：跳过多少条数据，默认值是 `0`，并且必须大于等于 `0`
- `limit`：返回多少条数据，默认值是 `10`，并且不能超过 `60`

然后在多个接口中通过 `Depends` 复用：

```python
@app.get("/news/news_list")
async def get_news_list(commons = Depends(common_parameters)):
    return commons

@app.get("/user/user_list")
async def get_user_list(commons = Depends(common_parameters)):
    return commons
```

注意：`Depends` 中传的是函数本身，不要加括号。

正确写法：

```python
Depends(common_parameters)
```

错误写法：

```python
Depends(common_parameters())
```

因为加了括号就变成了立即调用函数，而不是把函数交给 FastAPI 作为依赖项管理。

启动示例：

```powershell
uvicorn fastapi_file.depends:app --reload
```

访问：

```text
http://127.0.0.1:8000/news/news_list?skip=0&limit=10
http://127.0.0.1:8000/user/user_list?skip=5&limit=20
```

返回示例：

```json
{
  "skip": 0,
  "limit": 10
}
```

依赖注入的优点：

- 代码复用：一次编写，多处使用
- 解耦：业务逻辑和基础设施代码分离
- 易于测试：可以用模拟依赖替换真实依赖

## Redis 缓存

缓存是一种把常用数据暂时存放起来的机制。接口下一次需要同一份数据时，优先从缓存读取，避免每次都访问数据库。

在 Web 项目中，缓存的核心价值是减少重复查询，从而提升响应速度、降低网络延迟，并减轻数据库负载。常用流程如下：

```text
前端请求数据
-> 后端查询 Redis
-> 缓存命中：直接返回缓存数据
-> 缓存未命中：查询 MySQL -> 写入 Redis（设置过期时间）-> 返回数据
```

当前新闻项目在 `toutiao_backend/config/cache_conf.py` 中使用 `redis.asyncio` 创建异步客户端，并封装了下列操作：

| 方法 | 参数 | 作用 |
| --- | --- | --- |
| `get_cache` | `key` | 读取字符串缓存；缓存不存在时返回 `None` |
| `get_json_cache` | `key` | 读取并解析列表或字典缓存 |
| `set_cache` | `key`、`value`、`expire` | 写入缓存并设置过期时间，默认 3600 秒 |

写入列表或字典时，代码会用 `json.dumps()` 序列化；读取时再用 `json.loads()` 还原。这让 Redis 的字符串存储结构也能方便地保存 JSON 数据。

本地使用前先确保 Redis 服务已启动，并在当前 Python 环境安装依赖：

```powershell
pip install redis
```

本机 Redis 为 5.x，配置中指定 `protocol=2` 以兼容新版 `redis-py`。如果省略该参数，客户端可能默认发送 Redis 6 以后才支持的 `HELLO 3` 命令并连接失败。

## ORM 简介

ORM 全称是 `Object-Relational Mapping`，中文叫对象关系映射。

它是一种编程技术，用于在面向对象编程语言和关系型数据库之间建立映射。简单说，就是让开发者可以用操作 Python 对象的方式操作数据库，而不需要直接编写大量复杂 SQL。

例如，原本可能要写 SQL：

```sql
SELECT * FROM users WHERE id = 1;
```

使用 ORM 后，更像是在操作对象：

```python
user = await session.get(User, 1)
```

ORM 的优势：

- 减少重复 SQL 代码
- 代码更简洁易读
- 自动处理数据库连接和事务
- 能降低手写 SQL 时出现 SQL 注入问题的风险

常见 ORM 工具：

| 排名 | ORM 工具 | 特点 | 适用场景 |
| --- | --- | --- | --- |
| 1 | SQLAlchemy ORM | 功能最强、最灵活、企业级 | 各类 API、微服务、数据应用 |
| 2 | Django ORM | 封装好、上手快 | Django 项目、管理后台 |
| 3 | Tortoise ORM | 全异步 | 异步 Web 服务、高并发 API |

ORM 的基本使用流程：

```text
1. 安装 ORM 和数据库驱动
2. 建库、建表
3. 查询、新增、修改、删除数据
```

在 FastAPI 学习中，后续如果要连接数据库，常见组合是：

```text
FastAPI + SQLAlchemy + asyncmy
```

其中：

- `SQLAlchemy`：ORM 工具
- `asyncmy`：异步 MySQL 数据库驱动
- `run_sync(Base.metadata.create_all)`：常用于异步环境中创建数据库表

## SQLAlchemy 2.x 常用导入

SQLAlchemy 2.x 把 ORM 相关对象和异步数据库对象放在不同模块中。写 FastAPI + SQLAlchemy 异步 ORM 时，导入位置要分清楚。

ORM 模型常用导入：

```python
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
```

其中：

- `DeclarativeBase`：声明 ORM 基类
- `Mapped`：声明模型字段的 Python 类型
- `mapped_column`：声明数据库字段类型、约束和注释

异步数据库连接常用导入：

```python
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
```

其中：

- `create_async_engine`：创建异步数据库引擎
- `async_sessionmaker`：创建异步会话工厂
- `AsyncSession`：异步数据库会话类型

常见错误：

```python
from sqlalchemy import DeclarativeBase, Mapped, mapped_column
```

如果这样写后出现：

```text
ImportError: cannot import name 'DeclarativeBase' from 'sqlalchemy'
```

原因通常不是 SQLAlchemy 版本一定太旧，而是导入位置不对。应该改成：

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
```

字段定义推荐写法：

```python
class Category(Base):
    __tablename__ = "news_category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
```

注意不要写成：

```python
sort_order = Mapped[int] = mapped_column(Integer)
```

正确写法应该是类型标注：

```python
sort_order: Mapped[int] = mapped_column(Integer)
```

## SQLAlchemy 异步 ORM 建表示例

`orm_01.py` 演示了 FastAPI + SQLAlchemy 异步 ORM 操作 MySQL 的完整练习流程，当前包含自动建表、查询、模糊查询、聚合查询、分页查询、新增、更新和删除。

这个示例的核心结构是：

```text
读取数据库连接串 -> 创建异步引擎 -> 定义 ORM 模型 -> 注入数据库会话 -> 操作 book 表
```

### 连接串来源

代码会读取 `01_GitHub仓库文件/config/.env` 中的数据库连接串：

```text
ASYNC_DATABASE_URL=...
```

因为数据库连接串通常包含用户名、密码、主机和数据库名，所以 `config/.env` 不应该提交到 GitHub。当前仓库已经通过 `.gitignore` 忽略这个文件。

### 异步引擎和会话

`orm_01.py` 使用 `create_async_engine` 创建异步数据库引擎：

```python
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20
)
```

其中：

- `ASYNC_DATABASE_URL`：数据库连接地址
- `echo=True`：在终端输出执行的 SQL，学习阶段便于观察
- `pool_size=10`：连接池中保持的活跃连接数量
- `max_overflow=20`：连接池不够用时允许额外创建的连接数

数据库会话通过依赖注入交给接口函数使用：

```python
AsyncSessionlocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_database():
    async with AsyncSessionlocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

这里的 `Depends(get_database)` 会在每次请求时提供一个 `AsyncSession`，接口函数只负责写查询或增删改逻辑。

### 模型定义和启动建表

`Base` 是所有 ORM 模型类的基类，里面统一定义了创建时间和更新时间。`Book` 类对应数据库里的 `book` 表：

```python
class Book(Base):
    __tablename__ = "book"
    id: Mapped[int] = mapped_column(primary_key=True, comment="书籍ID")
    bookname: Mapped[str] = mapped_column(String(255), comment="书名")
    author: Mapped[str] = mapped_column(String(255), comment="作者")
    price: Mapped[float] = mapped_column(Float, comment="书籍价格")
    publisher: Mapped[str] = mapped_column(String(255), comment="出版社")
```

FastAPI 启动时通过 `lifespan` 调用 `create_tables()`：

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
```

`create_tables()` 内部通过：

```python
await conn.run_sync(Base.metadata.create_all)
```

把 ORM 模型定义同步成数据库表结构。

### 启动命令

如果终端在当前仓库总根目录：

```powershell
python -m uvicorn fastapi_file.orm_01:app --reload --app-dir ".\01_GitHub仓库文件"
```

如果已经先进入 `01_GitHub仓库文件` 目录：

```powershell
python -m uvicorn fastapi_file.orm_01:app --reload
```

启动成功后访问：

```text
http://127.0.0.1:8000/docs
```

可以在 FastAPI 交互式文档里测试下面这些接口。

### 查询全部数据

查询核心链路是：

```text
select() -> db.execute() -> scalars().all() -> 返回列表
```

代码示例：

```python
@app.get("/book/books")
async def get_book_list(db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(Book))
    book = result.scalars().all()
    return book
```

访问：

```text
http://127.0.0.1:8000/book/books
```

### 条件查询

按主键 id 查询单条数据：

```python
@app.get("/book/search_book_id/{book_id}")
async def get_book_list1(book_id: int, db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalars().first()
    return book
```

访问：

```text
http://127.0.0.1:8000/book/search_book_id/1
```

按价格查询多条数据：

```python
@app.get("/book/search_book_price/{price}")
async def get_book_list2(price: float, db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(Book).where(Book.price >= price))
    book = result.scalars().all()
    return book
```

访问：

```text
http://127.0.0.1:8000/book/search_book_price/100
```

### 模糊查询和逻辑条件

SQLAlchemy 中可以使用 `like()` 做模糊查询：

| 写法 | 含义 |
| --- | --- |
| `like("曹%")` | 以“曹”开头 |
| `like("%曹")` | 以“曹”结尾 |
| `like("%曹%")` | 包含“曹” |
| `like("曹_")` | “曹”后面匹配一个字符 |

SQL 通配符里，`%` 表示零个、一个或多个字符，`_` 表示一个单字符。这里不是 Python 里的 `*`。

当前代码把作者和价格作为查询参数，并使用 `&` 表示“同时满足”：

```python
@app.get("/book/search_book_author")
async def get_book_list3(
    author: str,
    price: float,
    db: AsyncSession = Depends(get_database)
):
    result = await db.execute(
        select(Book).where((Book.author.like(f"{author}%")) & (Book.price >= price))
    )
    book = result.scalars().all()
    return book
```

访问：

```text
http://127.0.0.1:8000/book/search_book_author?author=曹&price=100
```

常见逻辑符号：

| 符号 | 含义 |
| --- | --- |
| `&` | 与，同时满足 |
| `|` | 或，满足任意一个 |
| `~` | 非，取反 |

包含查询可以使用 `in_()`：

```python
id_list = [1, 3, 5, 7]
result = await db.execute(select(Book).where(Book.id.in_(id_list)))
```

访问：

```text
http://127.0.0.1:8000/book/search_book_author_idlist
```

### 聚合查询

聚合查询使用：

```text
func.方法(模型类.属性)
```

常用方法：

| 方法 | 作用 |
| --- | --- |
| `func.count(Book.id)` | 统计行数 |
| `func.avg(Book.price)` | 求平均值 |
| `func.max(Book.price)` | 求最大值 |
| `func.min(Book.price)` | 求最小值 |
| `func.sum(Book.price)` | 求和 |

当前代码示例返回最高价格：

```python
@app.get("/book/count")
async def get_count(db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(func.max(Book.price)))
    num = result.scalar()
    return num
```

这里使用 `scalar()`，因为聚合查询返回的是一个标量值，而不是一组 ORM 对象。

### 分页查询

分页查询核心是：

```text
select().offset().limit()
```

其中：

- `offset`：跳过的记录数
- `limit`：返回的记录数

计算公式：

```text
offset = (当前页码 - 1) * 每页数量
```

例如每页 10 条：

| 当前页码 | 每页数量 limit | 跳过数量 offset |
| --- | --- | --- |
| 1 | 10 | 0 |
| 2 | 10 | 10 |
| 3 | 10 | 20 |
| 4 | 10 | 30 |

当前分页接口：

```python
@app.get("/book/get_book_list")
async def get_book_list(
    page: int = 1,
    page_size: int = 3,
    db: AsyncSession = Depends(get_database)
):
    skip = (page - 1) * page_size
    result = await db.execute(select(Book).order_by(Book.id).offset(skip).limit(page_size))
    books = result.scalars().all()
    return books
```

访问：

```text
http://127.0.0.1:8000/book/get_book_list?page=1&page_size=3
http://127.0.0.1:8000/book/get_book_list?page=2&page_size=3
```

注意：查询多条 ORM 对象时使用 `scalars().all()`；聚合查询等单个标量值使用 `scalar()`。

### 新增数据

数据库新增的核心步骤：

```text
定义请求体模型 -> 创建 ORM 对象 -> add(对象) -> commit 提交到数据库
```

当前请求体模型：

```python
class BookBase(BaseModel):
    id: int
    bookname: str
    author: str
    price: float
    publisher: str
```

新增接口：

```python
@app.post("/book/add_book")
async def add_book(book: BookBase, db: AsyncSession = Depends(get_database)):
    book_obj = Book(**book.__dict__)
    db.add(book_obj)
    await db.commit()
    return book
```

测试请求体：

```json
{
  "id": 11,
  "bookname": "骆驼祥子",
  "author": "老舍",
  "price": 49,
  "publisher": "人民文学出版社"
}
```

### 更新数据

数据库更新的核心步骤：

```text
先 get 查询 -> 属性重新赋值 -> commit 提交到数据库
```

当前接口：

```python
@app.put("/book/update_book/{book_id}")
async def update_book(book_id: int, data: BookUpdate, db: AsyncSession = Depends(get_database)):
    db_book = await db.get(Book, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="查无此书")

    db_book.bookname = data.bookname
    db_book.author = data.author
    db_book.price = data.price
    db_book.publisher = data.publisher

    await db.commit()
    return db_book
```

访问：

```text
PUT http://127.0.0.1:8000/book/update_book/1
```

请求体：

```json
{
  "bookname": "Python ORM 实战",
  "author": "yuan",
  "price": 128,
  "publisher": "学习出版社"
}
```

如果使用 SQLAlchemy 的 `update()` 语句直接更新数据，可以通过 `rowcount` 判断是否真的命中了记录。

例如新闻详情页浏览量加 1：

```python
stmt = (
    update(News)
    .where(News.id == news_id)
    .values(views=News.views + 1)
)
result = await db.execute(stmt)
await db.commit()
return result.rowcount > 0
```

这里的 `return result.rowcount > 0` 很重要。否则函数执行完默认返回 `None`，如果路由层写了 `if not views_res:`，就会误判为更新失败，可能返回 404。

### 删除数据

数据库删除的核心步骤：

```text
先 get 查询 -> delete 删除 -> commit 提交到数据库
```

当前接口：

```python
@app.delete("/book/delete_book/{book_id}")
async def delete_book(book_id: int, db: AsyncSession = Depends(get_database)):
    db_book = await db.get(Book, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="查无此书")

    await db.delete(db_book)
    await db.commit()
    return {"message": "删除成功"}
```

访问：

```text
DELETE http://127.0.0.1:8000/book/delete_book/11
```

### ORM 查询总结

从 ORM 对象获取数据的常用方式：

| 写法 | 作用 | 常见场景 |
| --- | --- | --- |
| `scalars().all()` | 获取所有 ORM 对象 | 查询列表 |
| `scalars().first()` | 获取第一条 ORM 对象 | 查询单条，允许没有结果 |
| `scalar_one_or_none()` | 获取一个对象或 `None` | 期望最多一条结果 |
| `scalar()` | 获取标量值 | 聚合查询，例如 `count`、`max` |

整个 ORM 操作可以概括为：

```text
查询：select()
新增：add()
更新：先查再改，重新赋值
删除：delete()
提交：commit()
```
