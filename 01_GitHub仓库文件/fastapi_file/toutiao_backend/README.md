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
- 封装分类列表查询 CRUD
- 封装新闻列表、新闻数量、新闻详情、浏览量自增、相关新闻查询 CRUD
- 实现新闻分类列表接口
- 实现按分类分页查询新闻列表接口
- 实现新闻详情接口，并在进入详情页时浏览量加 1
- 实现同分类相关新闻推荐
- 导入新闻资讯项目数据库 `news_app`

当前接口：

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| `GET` | `/` | 健康检查，返回 hello world |
| `GET` | `/api/news/categories` | 获取新闻分类列表，支持 `skip` 和 `limit` 分页参数 |
| `GET` | `/api/news/list` | 按分类分页获取新闻列表，参数为 `categoryId`、`page`、`pageSize` |
| `GET` | `/api/news/detail` | 获取新闻详情，参数为 `id`；成功后浏览量自动加 1，并返回相关新闻 |

## 技术栈

| 技术 | 用途 |
| --- | --- |
| FastAPI | Web API 框架 |
| Uvicorn | ASGI 服务启动器 |
| SQLAlchemy 2.x | ORM 模型和数据库查询 |
| asyncmy | 异步 MySQL 驱动 |
| MySQL 8.0 | 项目数据库 |
| Pydantic | 后续用于请求体和响应模型校验 |

## 目录结构

```text
toutiao_backend/
├── README.md              # 项目实操说明
├── main.py                # FastAPI 应用入口，注册路由
├── database.sql           # 新闻项目数据库结构和初始化数据
├── config/
│   └── db_conf.py         # 异步数据库连接和会话依赖
├── crud/
│   └── news.py            # 新闻相关数据库操作
├── models/
│   └── news.py            # SQLAlchemy ORM 模型
├── routers/
│   └── news.py            # 新闻模块接口路由
├── schemas/               # 预留：Pydantic 请求/响应模型
└── utils/                 # 预留：通用工具函数
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

## 接口实现流程

### 1. 模块化路由

在 `routers/news.py` 中创建新闻模块路由：

```python
router = APIRouter(prefix="/api/news", tags=["news"])
```

`prefix` 表示统一路径前缀，`tags` 用于在 `/docs` 文档中分组。

### 2. 定义模型类

在 `models/news.py` 中用 SQLAlchemy 2.x 写 ORM 模型：

```python
class Category(Base):
    __tablename__ = "news_category"

class News(Base):
    __tablename__ = "news"
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

## 实操经验总结

- 先建数据库和表，再写 ORM 模型，模型字段要参考真实表结构。
- 一个接口不要直接把所有逻辑写在路由函数里，建议拆成 `routers -> crud -> models`。
- `Depends` 适合注入数据库会话，接口函数就不用关心连接创建和关闭。
- SQLAlchemy 2.x 的类型注解写法是 `字段名: Mapped[类型] = mapped_column(...)`。
- 查询列表常用 `result.scalars().all()`，查询单条常用 `result.scalars().first()`。
- 详情查询这类“最多一条”的场景，可以使用 `scalar_one_or_none()`。
- `update()` 之后如果路由层要判断成功失败，应检查 `rowcount`，不要依赖没有返回值的函数。
- `.env` 只保存本地密钥和连接串，README 只能写示例，不能写真实密码。

## 后续计划

- 补充 `schemas/` 中的 Pydantic 响应模型
- 实现收藏、浏览历史等用户行为接口
- 为接口返回统一响应结构
- 增加常见错误处理，例如分类不存在、新闻不存在
