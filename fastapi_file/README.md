# FastAPI 学习记录

这个文件夹用于记录 FastAPI 的基础用法示例，当前主要包含：

- `first.py`：路由、路径参数、查询参数示例
- `sync_async.py`：同步接口和异步接口耗时对比示例

## 怎么运行 FastAPI 项目

推荐在项目根目录运行：

```powershell
uvicorn fastapi_file.first:app --reload
```

如果要运行同步/异步耗时对比示例：

```powershell
uvicorn fastapi_file.sync_async:app --reload
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
