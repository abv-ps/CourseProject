"""
FastAPI router module for managing author-related HTTP endpoints.

This module provides RESTful API endpoints to create, read, update,
delete authors, and fetch their related books. It integrates with
asynchronous CRUD utilities and sends Kafka notifications upon
author creation and updates.

Endpoints:
- POST /authors/: Create a new author.
- GET /authors/: List all authors.
- GET /authors/{author_id}: Retrieve a single author by ID.
- DELETE /authors/{author_id}: Delete an author by ID.
- PATCH /authors/{author_id}: Update author fields by ID.
- GET /authors/{author_id}/books: List books by a specific author.
- GET /authors/books: List books by multiple authors.

Dependencies:
- BackgroundTasks for asynchronous background job processing.
- KafkaProducerService to send Kafka events.
"""

from fastapi import APIRouter, BackgroundTasks, HTTPException
from typing import Optional, List, Dict, Any

from app.crud.items import (
    get_item,
    delete_item,
    list_items,
    update_item,
    get_author_books,
)
from app.crud.author import create_author
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorRead
from app.schemas.book import BookRead
from app.kafka.producer import kafka_producer

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.post("/", response_model=AuthorCreate)
async def create(author: AuthorCreate, background_tasks: BackgroundTasks) -> AuthorCreate:
    """
    Create a new author and send a Kafka notification.

    Args:
        author (AuthorCreate): Author creation payload.
        background_tasks (BackgroundTasks): FastAPI background task handler.

    Returns:
        AuthorCreate: The created author data.
    """
    result = await create_author(Author(**author.model_dump()), background_tasks)
    await kafka_producer.send_event(
        key="author_created",
        payload={"author_id": result.author_id, "name": result.author_name},
    )
    return result


@router.get("/", response_model=List[AuthorRead])
async def list_all() -> List[AuthorRead]:
    """
    Retrieve all authors.

    Returns:
        List[AuthorRead]: List of all authors.
    """
    return await list_items(Author)


@router.get("/{author_id}", response_model=AuthorRead)
async def get(author_id: int) -> AuthorRead:
    """
    Retrieve a single author by ID.

    Args:
        author_id (int): Author's ID.

    Raises:
        HTTPException: 404 if author not found.

    Returns:
        AuthorRead: The found author.
    """
    author = await get_item(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.delete("/{author_id}")
async def delete(author_id: int) -> dict[str, int]:
    """
    Delete an author by ID.

    Args:
        author_id (int): Author's ID.

    Returns:
        dict: Confirmation of deletion.
    """
    await delete_item(Author, author_id)
    return {"deleted": author_id}


@router.patch("/{author_id}", response_model=AuthorRead)
async def update(author_id: int, update_data: Dict[str, Any]) -> AuthorRead:
    """
    Update author fields by ID and send Kafka notification.

    Args:
        author_id (int): Author's ID.
        update_data (Dict[str, Any]): Fields to update.

    Raises:
        HTTPException: 404 if author not found.

    Returns:
        AuthorRead: Updated author data.
    """
    updated = await update_item(Author, author_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Author not found")
    await kafka_producer.send_event(
        key="author_updated",
        payload={"author_id": updated.author_id, "name": updated.author_name},
    )
    return updated


@router.get("/{author_id}/books", response_model=List[BookRead])
async def get_books_by_author(author_id: int) -> List[BookRead]:
    """
    Retrieve books related to a single author.

    Args:
        author_id (int): Author's ID.

    Returns:
        List[BookRead]: List of books by the author.
    """
    return await get_author_books(author_id=author_id)


@router.get("/books", response_model=List[BookRead])
async def get_books_by_multiple_authors(author_ids: Optional[List[int]] = None) -> List[BookRead]:
    """
    Retrieve books related to multiple authors.

    Args:
        author_ids (Optional[List[int]]): List of author IDs.

    Returns:
        List[BookRead]: List of books by the specified authors.
    """
    return await get_author_books(author_ids=author_ids)
