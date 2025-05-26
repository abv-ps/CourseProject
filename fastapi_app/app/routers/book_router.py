"""
FastAPI router module for managing book-related HTTP endpoints.

This module provides asynchronous RESTful API endpoints to create,
read, update, delete books, and integrates Kafka event notifications
on creation and update events.

Endpoints:
- POST /books/: Create a new book.
- GET /books/: List all books.
- GET /books/{book_id}: Retrieve a book by its ID.
- DELETE /books/{book_id}: Delete a book by its ID.
- PATCH /books/{book_id}: Update book fields by its ID.

Dependencies:
- BackgroundTasks for asynchronous background processing.
- KafkaProducerService to send Kafka events.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Any

from app.crud.items import get_item, delete_item, list_items, update_item
from app.crud.book import create_book
from app.schemas.book import BookCreate, BookRead
from app.models.book import Book
from app.kafka.producer import kafka_producer

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=Book)
async def create(book: BookCreate, background_tasks: BackgroundTasks) -> Book:
    """
    Create a new book and send a Kafka notification.

    Args:
        book (BookCreate): Book creation payload.
        background_tasks (BackgroundTasks): FastAPI background tasks.

    Returns:
        Book: Created book instance.
    """
    result = await create_book(Book(**book.model_dump()), background_tasks)
    await kafka_producer.send_event(
        key="book_created",
        payload={"book_id": result.book_id, "title": result.title},
    )
    return result


@router.get("/", response_model=List[BookRead])
async def list_all() -> List[BookRead]:
    """
    Retrieve all books.

    Returns:
        List[BookRead]: List of all books.
    """
    return await list_items(Book)


@router.get("/{book_id}", response_model=BookRead)
async def get(book_id: int) -> BookRead:
    """
    Retrieve a book by ID.

    Args:
        book_id (int): Book's ID.

    Raises:
        HTTPException: 404 if book not found.

    Returns:
        BookRead: Book instance.
    """
    book = await get_item(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.delete("/{book_id}")
async def delete(book_id: int) -> dict[str, int]:
    """
    Delete a book by ID.

    Args:
        book_id (int): Book's ID.

    Returns:
        dict: Confirmation of deletion.
    """
    await delete_item(Book, book_id)
    return {"deleted": book_id}


@router.patch("/{book_id}", response_model=BookRead)
async def update(book_id: int, update_data: Dict[str, Any]) -> BookRead:
    """
    Update book fields by ID and send Kafka notification.

    Args:
        book_id (int): Book's ID.
        update_data (Dict[str, Any]): Fields to update.

    Raises:
        HTTPException: 404 if book not found.

    Returns:
        BookRead: Updated book instance.
    """
    updated = await update_item(Book, book_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    await kafka_producer.send_event(
        key="book_updated",
        payload={"book_id": updated.book_id, "title": updated.title},
    )
    return updated
