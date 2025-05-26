"""
Asynchronous database connection and session management using SQLAlchemy.

This module sets up an asynchronous SQLAlchemy engine and session maker for Postgres
using environment variables for configuration. It provides an async generator
to yield database sessions for dependency injection or direct use.

Constants:
- DATABASE_URL: Async connection URL for the Postgres database.
- SQLALCHEMY_URL: Synchronous connection URL for compatibility purposes.

Variables:
- engine: Async SQLAlchemy engine instance.
- async_session: Async session maker factory for creating AsyncSession instances.

Functions:
- get_db: Async generator that yields an AsyncSession instance, handling session lifecycle.
"""

import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DB_USER: str = os.getenv("FASTAPI_POSTGRES_USER", "postgres")
DB_PASSWORD: str = os.getenv("FASTAPI_POSTGRES_PASSWORD", "postgres")
DB_HOST: str = os.getenv("FASTAPI_POSTGRES_HOST", "localhost")
DB_PORT: str = os.getenv("FASTAPI_POSTGRES_PORT", "5433")
DB_NAME: str = os.getenv("FASTAPI_POSTGRES_DB", "booksdb")

DATABASE_URL: str = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
SQLALCHEMY_URL: str = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Async generator yielding an SQLAlchemy AsyncSession.

    This function manages the lifespan of the database session, ensuring
     the proper opening and closing of the session in an async context.

    Yields:
        AsyncSession: An instance of AsyncSession for database operations.
    """
    async with async_session() as session:
        yield session
