import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DB_USER = os.getenv("FASTAPI_POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("FASTAPI_POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("FASTAPI_POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("FASTAPI_POSTGRES_PORT", "5433")
DB_NAME = os.getenv("FASTAPI_POSTGRES_DB", "booksdb")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SQLALCHEMY_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with async_session() as session:
        yield session
