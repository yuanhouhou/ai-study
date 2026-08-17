# toutiao_backend 新闻资讯后端项目实操

这个目录记录一个新闻资讯类 FastAPI 后端项目的实操过程。它不是单纯的语法示例，而是把模块化路由、SQLAlchemy ORM、MySQL 数据库和接口调用流程串起来，逐步形成一个可运行的小型后端项目。

当前项目已经跑通了新闻首页到详情页的核心业务链路：

```text
客户端请求 -> APIRouter 路由 -> Depends 注入数据库会话 -> CRUD 查询 -> ORM 模型映射 -> MySQL 返回数据 -> 接口响应
```

## 项目定位

- `toutiao_backend/README.md`：记录这个新闻后端项目的功能、结构、运行方式、数据库、接口和实操经验。
- `../README.md`：记录 FastAPI 学习知识点，例如路由、依赖注入、ORM、异步数据库会话等。

## 当前功能

已完成：

- 搭建 FastAPI 应用入口 `main.py`
- 使用 `APIRouter` 拆分新闻模块路由
- 配置 CORS，允许前端开发服务跨域访问后端接口
- 连接 MySQL 异步数据库
- 使用 SQLAlchemy 2.x ORM 定义 `news_category` 分类模型
- 使用 SQLAlchemy 2.x ORM 定义 `news` 新闻模型
- 使用 SQLAlchemy 2.x ORM 定义 `user` 和 `user_token` 用户模型
- 封装分类列表查询 CRUD
- 封装新闻列表、新闻数量、新闻详情、浏览量自增、相关新闻查询 CRUD
- 封装用户查询、用户创建、Token 创建或更新、用户信息更新、密码修改 CRUD
- 封装收藏状态查询、添加收藏、取消收藏 CRUD
- 使用 `bcrypt` 对注册密码加密存储
- 使用 `uuid.uuid4()` 生成临时访问令牌 Token
- 使用 Pydantic 定义用户认证、用户资料更新、修改密码和收藏接口请求/响应模型
- 封装 `success_response()` 统一接口响应结构
- 注册全局异常处理器，统一处理业务异常、数据库完整性异常和服务器内部异常
- 抽取 `get_current_user()` 依赖，通过 `Authorization` 请求头校验 Token 并获取当前用户
- 实现新闻分类列表接口
- 实现按分类分页查询新闻列表接口
- 实现新闻详情接口，并在进入详情页时浏览量加 1
- 实现同分类相关新闻推荐
- 实现用户注册接口：检查用户名是否存在，不存在则创建用户并返回 Token
- 实现用户登录接口：校验密码并返回 Token
- 实现获取当前用户信息接口
- 实现修改用户资料接口
- 实现修改密码接口
- 实现收藏状态检查、添加收藏、取消收藏接口
- 导入新闻资讯项目数据库 `news_app`

当前接口：

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| `GET` | `/` | 健康检查，返回 hello world |
| `GET` | `/api/news/categories` | 获取新闻分类列表，支持 `skip` 和 `limit` 分页参数 |
| `GET` | `/api/news/list` | 按分类分页获取新闻列表，参数为 `categoryId`、`page`、`pageSize` |
| `GET` | `/api/news/detail` | 获取新闻详情，参数为 `id`；成功后浏览量自动加 1，并返回相关新闻 |
| `POST` | `/api/user/register` | 用户注册，提交 `username`、`password`，成功后返回 Token 和用户信息 |
| `POST` | `/api/user/login` | 用户登录，提交 `username`、`password`，成功后返回 Token 和用户信息 |
| `GET` | `/api/user/info` | 获取当前登录用户信息，需要 `Authorization` 请求头 |
| `PUT` | `/api/user/update` | 修改当前用户资料，需要 `Authorization` 请求头 |
| `PUT` | `/api/user/password` | 修改当前用户密码，需要 `Authorization` 请求头 |
| `GET` | `/api/favorite/check` | 检查新闻是否已收藏，参数为 `newsId`，需要 `Authorization` 请求头 |
| `POST` | `/api/favorite/add` | 添加收藏，请求体参数为 `newsId`，需要 `Authorization` 请求头 |
| `DELETE` | `/api/favorite/remove` | 取消收藏，参数为 `newsId`，需要 `Authorization` 请求头 |

## 技术栈

| 技术 | 用途 |
| --- | --- |
| FastAPI | Web API 框架 |
| Uvicorn | ASGI 服务启动器 |
| SQLAlchemy 2.x | ORM 模型和数据库查询 |
| asyncmy | 异步 MySQL 驱动 |
| MySQL 8.0 | 项目数据库 |
| Pydantic | 请求体和响应模型校验 |
| bcrypt | 密码哈希加密 |
| uuid | 生成临时访问令牌 Token |

## 目录结构

```text
toutiao_backend/
├── README.md              # 项目实操说明
├── main.py                # FastAPI 应用入口，注册路由
├── database.sql           # 新闻项目数据库结构和初始化数据
├── config/
│   └── db_conf.py         # 异步数据库连接和会话依赖
├── crud/
│   ├── favorite.py        # 收藏相关数据库操作
│   ├── news.py            # 新闻相关数据库操作
│   └── users.py           # 用户认证、资料和 Token 相关数据库操作
├── models/
│   ├── favorite.py        # 收藏 SQLAlchemy ORM 模型
│   ├── news.py            # 新闻相关 SQLAlchemy ORM 模型
│   └── users.py           # 用户和 Token SQLAlchemy ORM 模型
├── routers/
│   ├── favorite.py        # 收藏模块接口路由
│   ├── news.py            # 新闻模块接口路由
│   └── users.py           # 用户模块接口路由
├── schemas/
│   ├── favorite.py        # 收藏请求和响应 Pydantic 模型
│   └── users.py           # 用户请求和响应 Pydantic 模型
└── utils/
    ├── auth.py            # Token 认证依赖
    ├── exception.py       # 全局异常处理函数
    ├── exception_handlers.py # 异常处理器注册入口
    ├── response.py        # 统一响应结构
    └── security.py        # 密码加密和校验
```

## 数据库说明

数据库初始化文件是：

```text
database.sql
```

它会创建数据库：

```sql
CREATE DATABASE IF NOT EXISTS news_app DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE news_app;
```

当前数据库包含的表：

| 表名 | 说明 |
| --- | --- |
| `user` | 用户信息表 |
| `user_token` | 用户令牌表 |
| `news_category` | 新闻分类表 |
| `news` | 新闻表 |
| `related_news` | 相关新闻关联表 |
| `favorite` | 收藏表 |
| `history` | 浏览历史表 |
| `ai_chat` | AI 聊天记录表 |

当前已验证的数据量：

| 表名 | 数据量 |
| --- | --- |
| `news_category` | 8 |
| `news` | 403 |
| `user` | 1 |

其他表目前主要用于后续功能扩展。

## 本地配置

数据库连接信息从本地配置文件读取：

```text
01_GitHub仓库文件/config/.env
```

这个文件包含数据库用户名和密码，不能提交到 GitHub。仓库 `.gitignore` 已经忽略 `.env` 文件。

示例配置格式：

```env
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=你的密码
MYSQL_DATABASE=news_app
ASYNC_DATABASE_URL=mysql+asyncmy://用户名:密码@127.0.0.1:3306/news_app?charset=utf8mb4
```

当前 `config/db_conf.py` 会读取 `ASYNC_DATABASE_URL`，并连接到 `news_app` 数据库。

## 数据库导入

确认 MySQL 服务已经启动：

```powershell
sc.exe query MySQL80
```

如果看到：

```text
STATE              : 4  RUNNING
```

说明 MySQL 已经运行。

导入数据库：

```powershell
cd .\01_GitHub仓库文件\fastapi_file\toutiao_backend
mysql -u root -p --default-character-set=utf8mb4 < database.sql
```

如果 `mysql` 命令不在 PATH 中，可以使用 MySQL 安装目录下的完整路径。

## 运行项目

进入项目目录：

```powershell
cd .\01_GitHub仓库文件\fastapi_file\toutiao_backend
```

启动服务：

```powershell
python -m uvicorn main:app --reload
```

也可以直接运行：

```powershell
python main.py
```

启动后访问：

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/api/news/categories
http://127.0.0.1:8000/docs
```

分类接口支持分页参数：

```text
http://127.0.0.1:8000/api/news/categories?skip=0&limit=8
```

新闻列表接口示例：

```text
http://127.0.0.1:8000/api/news/list?categoryId=1&page=1&pageSize=10
```

新闻详情接口示例：

```text
http://127.0.0.1:8000/api/news/detail?id=2
```

用户注册接口示例：

```text
POST http://127.0.0.1:8000/api/user/register
```

请求体：

```json
{
  "username": "example_user",
  "password": "123"
}
```

成功响应结构：

```json
{
  "code": 200,
  "message": "注册成功",
  "data": {
    "token": "uuid生成的访问令牌",
    "userInfo": {
      "id": 1,
      "username": "example_user",
      "nickname": null,
      "avatar": "https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg",
      "gender": "unknown",
      "bio": "这个人很懒，什么都没留下"
    }
  }
}
```

用户登录接口示例：

```text
POST http://127.0.0.1:8000/api/user/login
```

请求体：

```json
{
  "username": "example_user",
  "password": "123"
}
```

后续需要登录态的接口，都要在请求头中携带登录或注册返回的 Token：

```text
Authorization: uuid生成的访问令牌
```

获取当前用户信息：

```text
GET http://127.0.0.1:8000/api/user/info
```

修改用户资料：

```text
PUT http://127.0.0.1:8000/api/user/update
```

请求体示例：

```json
{
  "nickname": "yuan",
  "bio": "正在学习 FastAPI 新闻项目"
}
```

修改密码：

```text
PUT http://127.0.0.1:8000/api/user/password
```

请求体示例：

```json
{
  "oldPassword": "123",
  "newPassword": "123456"
}
```

收藏接口示例：

```text
GET http://127.0.0.1:8000/api/favorite/check?newsId=2
POST http://127.0.0.1:8000/api/favorite/add
DELETE http://127.0.0.1:8000/api/favorite/remove?newsId=2
```

添加收藏请求体：

```json
{
  "newsId": 2
}
```

## 接口实现流程

### 1. 模块化路由

在 `routers/news.py` 中创建新闻模块路由：

```python
router = APIRouter(prefix="/api/news", tags=["news"])
```

`prefix` 表示统一路径前缀，`tags` 用于在 `/docs` 文档中分组。

用户模块使用独立路由前缀：

```python
router = APIRouter(prefix="/api/user", tags=["users"])
```

收藏模块使用独立路由前缀：

```python
router = APIRouter(prefix="/api/favorite", tags=["favorite"])
```

### 2. 定义模型类

在 `models/news.py` 中用 SQLAlchemy 2.x 写 ORM 模型：

```python
class Category(Base):
    __tablename__ = "news_category"

class News(Base):
    __tablename__ = "news"

class User(Base):
    __tablename__ = "user"

class UserToken(Base):
    __tablename__ = "user_token"

class Favorite(Base):
    __tablename__ = "favorite"
```

模型类和数据库表对应，类属性和字段对应。

`News` 模型中使用索引提升常见查询速度：

```python
__table_args__ = (
    Index("fk_news_category_idx", "category_id"),
    Index("idx_publish_time", "publish_time"),
)
```

### 3. 封装 CRUD

在 `crud/news.py` 中写数据库查询逻辑：

```python
stmt = select(Category).offset(skip).limit(limit)
result = await db.execute(stmt)
return result.scalars().all()
```

CRUD 层只负责数据库操作，不直接处理路由响应格式。

新闻列表接口按分类查询，并使用 `offset()` 和 `limit()` 做分页：

```python
stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
```

新闻详情接口会先查详情，再执行浏览量自增：

```python
stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
result = await db.execute(stmt)
await db.commit()
return result.rowcount > 0
```

这里返回 `result.rowcount > 0` 很关键：它表示本次更新是否真的命中了新闻记录。

用户注册接口的核心 CRUD 流程：

```text
select(User).where(User.username == username)
-> 用户存在：抛出 400
-> 用户不存在：加密密码，创建 User
-> uuid.uuid4() 生成 Token
-> user_token 表新增或更新 Token
```

密码加密使用 `bcrypt.hashpw()`：

```python
password_bytes = password.encode("utf-8")
hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
```

Token 有效期当前设置为 7 天：

```python
expires_at = datetime.now() + timedelta(days=7)
```

收藏接口的核心 CRUD 流程：

```text
检查收藏：select(Favorite).where(user_id, news_id)
添加收藏：创建 Favorite 对象 -> add() -> commit() -> refresh()
取消收藏：delete(Favorite).where(user_id, news_id) -> commit() -> 检查 rowcount
```

### 4. 路由调用逻辑

在 `routers/news.py` 中通过 `Depends(get_db)` 获取数据库会话，然后调用 CRUD：

```python
categories = await news.get_categories(db, skip, limit)
```

接口函数负责接收参数、调用业务逻辑、组织响应结果。

详情接口使用查询参数 `id`：

```python
@router.get("/detail")
async def get_news_list(
    news_id: int = Query(..., alias="id"),
    db: AsyncSession = Depends(get_db)
):
    ...
```

所以正确访问方式是：

```text
/api/news/detail?id=2
```

如果把参数名写成 `Id` 或其他大小写，FastAPI 会认为缺少必填参数。

注册接口使用请求体参数：

```python
class UserRequest(BaseModel):
    username: str
    password: str
```

响应数据通过 Pydantic 模型组织，再交给统一响应函数：

```python
response_data = UserAuthResponse(
    token=token,
    user_info=UserInfoResponse.model_validate(user),
)
return success_response(message="注册成功", data=response_data)
```

## 已解决的问题

### SQLAlchemy 2.x 导入位置

`DeclarativeBase`、`Mapped`、`mapped_column` 应该从 `sqlalchemy.orm` 导入：

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
```

异步引擎和异步会话应该从 `sqlalchemy.ext.asyncio` 导入：

```python
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
```

### 数据库名不一致

`database.sql` 创建的是 `news_app`，所以后端连接也应该指向 `news_app`。如果连接到旧库名，接口会出现表不存在或数据为空的问题。

### 中文路径导入 SQL

某些 MySQL 客户端在执行 `source` 时可能不能正确处理中文路径。遇到这种情况，可以先进入 SQL 文件所在目录，再使用相对路径导入：

```powershell
cd .\01_GitHub仓库文件\fastapi_file\toutiao_backend
mysql -u root -p --default-character-set=utf8mb4 < database.sql
```

### 浏览量增加后仍然报 404

问题表现：

```json
{"detail": "浏览量增加失败"}
```

原因是 CRUD 函数执行了 `update()` 和 `commit()`，但没有返回值。Python 函数默认返回 `None`，路由层写了：

```python
if not views_res:
    raise HTTPException(status_code=404, detail="浏览量增加失败")
```

因此即使数据库已经更新成功，`None` 也会被判断为失败。

修复方式是在 CRUD 层返回更新是否命中记录：

```python
return result.rowcount > 0
```

### Swagger 中详情接口出现两个 id 参数

如果路由函数里同时写了两个 `Query` 参数，例如同时兼容 `id` 和 `Id`，FastAPI 的 `/docs` 会把它们都展示出来。当前项目统一使用前端传来的小写 `id`，所以详情接口只保留一个参数：

```python
news_id: int = Query(..., alias="id")
```

### 注册时 bcrypt 误报 72 bytes

问题表现：

```text
ValueError: password cannot be longer than 72 bytes
```

如果密码确实超过 72 bytes，这是 bcrypt 的算法限制。但本项目中曾经出现过密码为 `123` 也报这个错误，原因是 `passlib` 和新版 `bcrypt` 的兼容问题。

当前处理方式是直接使用 `bcrypt`：

```python
bcrypt.hashpw(password_bytes, bcrypt.gensalt())
```

同时在加密前显式检查字节长度：

```python
if len(password_bytes) > 72:
    raise ValueError("密码不能超过72字节")
```

### datetime.now 导入方式错误

如果写了：

```python
import datetime
expires_at = datetime.now()
```

会报：

```text
AttributeError: module 'datetime' has no attribute 'now'
```

因为此时 `datetime` 是模块，正确写法之一是：

```python
from datetime import datetime, timedelta
expires_at = datetime.now() + timedelta(days=7)
```

### success_response 导入失败

如果出现：

```text
ImportError: cannot import name 'success_response' from 'utils.response'
```

说明 `utils/response.py` 中没有定义同名函数，或者文件还没保存到当前运行的后端环境。当前项目已在 `utils/response.py` 中定义：

```python
def success_response(message: str = "success", data=None):
    ...
```

### HTTPException 大小写写错

FastAPI 中的异常类名是 `HTTPException`，不是 `HttpException`。Python 区分大小写，如果写成：

```python
from fastapi import HttpException
```

会在模块导入阶段报错。正确写法是：

```python
from fastapi import HTTPException
```

### Authorization 请求头处理

需要登录态的接口通过依赖项 `get_current_user()` 获取当前用户。`Authorization` 请求头建议先设置为可选，再在函数内部主动判断：

```python
authorization: Optional[str] = Header(None, alias="Authorization")

if not authorization:
    raise HTTPException(status_code=401, detail="未登录")
```

这样缺少 Token 时会返回清晰的 `401 未登录`，不会先触发请求参数校验错误。

### Pydantic 字段别名

前端常用小驼峰字段，例如 `newsId`、`oldPassword`、`newPassword`；Python 代码中更适合使用下划线命名，例如 `news_id`、`old_password`、`new_password`。可以使用 `Field(..., alias="前端字段名")` 做映射：

```python
class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")
```

这样前端传 `newsId`，后端函数内部仍然使用 `data.news_id`。

## 实操经验总结

- 先建数据库和表，再写 ORM 模型，模型字段要参考真实表结构。
- 一个接口不要直接把所有逻辑写在路由函数里，建议拆成 `routers -> crud -> models`。
- `Depends` 适合注入数据库会话，接口函数就不用关心连接创建和关闭。
- SQLAlchemy 2.x 的类型注解写法是 `字段名: Mapped[类型] = mapped_column(...)`。
- 查询列表常用 `result.scalars().all()`，查询单条常用 `result.scalars().first()`。
- 详情查询这类“最多一条”的场景，可以使用 `scalar_one_or_none()`。
- `update()` 之后如果路由层要判断成功失败，应检查 `rowcount`，不要依赖没有返回值的函数。
- 注册、登录这类接口建议统一返回 `code`、`message`、`data`，前端处理会更稳定。
- Token 是后端发给前端的访问令牌，前端保存后可以在后续请求中携带，用来证明“已经登录过”。
- 需要登录态的接口统一使用 `Depends(get_current_user)`，避免每个路由重复解析 Token。
- 前端字段名和后端 Python 变量名不一致时，用 Pydantic `Field(alias=...)` 保持两边命名习惯。
- 添加、取消收藏这类用户行为接口，要同时用 `user_id` 和 `news_id` 限定，避免影响其他用户的数据。
- ORM 字段默认时间建议传 `datetime.now` 函数本身，不要写成 `datetime.now()`，避免所有记录共用导入时的时间。
- `.env` 只保存本地密钥和连接串，README 只能写示例，不能写真实密码。

## 后续计划

- 继续完善收藏列表接口，支持查看当前用户收藏过的新闻。
- 实现浏览历史接口，记录和查询用户阅读记录。
- 补充用户资料更新、修改密码和收藏模块的接口联调记录。
- 增加更细的错误处理，例如收藏重复、新闻不存在、Token 过期提示。
