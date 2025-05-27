import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+asyncpg://admin:secret@localhost:5432/user_db"
)

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session