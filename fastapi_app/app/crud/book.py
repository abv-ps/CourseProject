"""
Module providing asynchronous CRUD operations for the Book model.

This module enables creation, retrieval, update, and deletion of Book records
using asynchronous SQLAlchemy sessions integrated with FastAPI. It also
supports background notifications upon creating a new book using FastAPI's
BackgroundTasks system.

Functions:
- create_book: Adds a new book and triggers a notification in the background.
- list_books: Retrieves all books.
- get_book: Fetches a book by ID.
- delete_book: Removes a book by ID.
- update_book: Updates a book's details by ID.
"""

from typing import List, Optional, Dict, Any

from fastapi import BackgroundTasks
from app.models.book import Book
from app.crud.items import (
    get_item,
    delete_item,
    list_items,
    update_item,
    send_notification
)
from app.db.session import async_session


async def create_book(book: Book, background_tasks: BackgroundTasks) -> Book:
    """
    Create a new book in the database and send a notification as a background task.

    Args:
        book (Book): Book instance to be created.
        background_tasks (BackgroundTasks): FastAPI background tasks instance.

    Returns:
        Book: The created book with updated database state.
    """
    async with async_session() as session:
        session.add(book)
        await session.commit()
        await session.refresh(book)

    background_tasks.add_task(send_notification, Book, book.title, book.book_id)
    return book


async def list_books() -> List[Book]:
    """
    Retrieve all books from the database.

    Returns:
        List[Book]: List of all books.
    """
    return await list_items(Book)


async def get_book(item_id: int) -> Optional[Book]:
    """
    Retrieve a book by its ID.

    Args:
        item_id (int): The ID of the book to retrieve.

    Returns:
        Optional[Book]: The requested book if found, otherwise None.
    """
    return await get_item(Book, item_id)


async def delete_book(item_id: int) -> None:
    """
    Delete a book by its ID.

    Args:
        item_id (int): The ID of the book to delete.
    """
    await delete_item(Book, item_id)


async def update_book(item_id: int, update_data: Dict[str, Any]) -> Optional[Book]:
    """
    Update a book by its ID with the provided data.

    Args:
        item_id (int): The ID of the book to update.
        update_data (Dict[str, Any]): Fields and values to update.

    Returns:
        Optional[Book]: The updated book if the update is successful, otherwise None.
    """
    return await update_item(Book, item_id, update_data)
