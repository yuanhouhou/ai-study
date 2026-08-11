from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from pathlib import Path
import os

#1.创建异步引擎

env_path = Path(__file__).resolve().parents[3] / "config" / ".env"
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("ASYNC_DATABASE_URL="):
            os.environ["ASYNC_DATABASE_URL"] = line.split("=", 1)[1].strip().replace(
                "/fastapi_orm_demo?", "/news_app?"
            )

ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL", "")
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo = True,#可选，输出sql日志
    pool_size = 10,#设置连接池活跃的连接数
    max_overflow = 20#允许额外的连接数
)

#2.创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind = async_engine,
    class_ = AsyncSession,
    expire_on_commit = False
)

#依赖项,用于获取数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise
        finally:
            await session.close()
