# FastAPI 学习记录

这个文件夹用于记录 FastAPI 的基础用法示例，当前主要包含：

- `first.py`：路由、路径参数、查询参数示例
- `sync_async.py`：同步接口和异步接口耗时对比示例
- `middleware.py`：中间件的定义和多个中间件的执行顺序示例
- `depends.py`：依赖注入系统示例，复用分页查询参数逻辑

## 目录

- [怎么运行 FastAPI 项目](#怎么运行-fastapi-项目)
- [怎么访问交互式文档](#怎么访问交互式文档)
- [路由是什么](#路由是什么)
- [参数的作用](#参数的作用)
- [参数分类](#参数分类)
- [路径参数](#路径参数)
- [查询参数](#查询参数)
- [同步和异步接口耗时对比](#同步和异步接口耗时对比)
- [请求体参数](#请求体参数)
- [请求体字段校验](#请求体字段校验)
- [响应类型](#响应类型)
- [响应数据模型](#响应数据模型)
- [异常处理](#异常处理)
- [中间件](#中间件)
- [依赖注入](#依赖注入)
- [ORM 简介](#orm-简介)

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
FastAPI + SQLAlchemy + aiomysql
```

其中：

- `SQLAlchemy`：ORM 工具
- `aiomysql`：异步 MySQL 数据库驱动
- `run_sync(Base.metadata.create_all)`：常用于异步环境中创建数据库表
