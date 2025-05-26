"""
This module initializes the FastAPI application for the Library API service.
It includes routers for authors and books management, sets up Kafka producer lifecycle,
and ensures proper disposal of the database engine upon shutdown.

The app provides endpoints for CRUD operations on authors and books,
and communicates with external systems via Kafka.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from collections.abc import AsyncGenerator

from app.kafka.producer import kafka_producer
from app.db.session import engine
from app.routers.author_router import router as author_router
from app.routers.book_router import router as book_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Async context manager for FastAPI application lifecycle.

    Starts the Kafka producer on startup and stops it on shutdown.
    Also disposes the SQLAlchemy engine on shutdown.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None
    """
    await kafka_producer.start()
    try:
        yield
    finally:
        await kafka_producer.stop()
        await engine.dispose()


app: FastAPI = FastAPI(
    title="Library API",
    description="API for managing authors and books",
    version="1.1.0",
    lifespan=lifespan,
)

app.include_router(author_router)
app.include_router(book_router)
