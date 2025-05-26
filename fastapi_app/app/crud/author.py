"""
Module for asynchronous CRUD operations on the Author model.

This module provides functions to create, read, update, and delete Author records
using asynchronous database sessions with SQLAlchemy and FastAPI. It also integrates
FastAPI's background task system to send notifications after creating a new author.

Functions:
- create_author: Adds a new author to the database and triggers a background notification.
- list_authors: Retrieves all authors from the database.
- get_author: Retrieves a single author by ID.
- delete_author: Deletes an author by ID.
- update_author: Updates an author's details by ID.

The module depends on reusable CRUD utilities from the `app.crud.items` module
and uses the asynchronous session from `app.db.session`.
"""

from typing import List, Optional

from fastapi import BackgroundTasks
from app.models.author import Author
from app.crud.items import (
    get_item,
    delete_item,
    list_items,
    update_item,
    send_notification
)
from app.db.session import async_session


async def create_author(author: Author, background_tasks: BackgroundTasks) -> Author:
    """
    Create a new author in the database and send a background notification.

    Args:
        author (Author): The author instance to be created.
        background_tasks (BackgroundTasks): FastAPI background tasks handler.

    Returns:
        Author: The created author instance with refreshed data.
    """
    async with async_session() as session:
        session.add(author)
        await session.commit()
        await session.refresh(author)

    background_tasks.add_task(send_notification, Author, author.author_name, author.author_id)
    return author


async def list_authors() -> List[Author]:
    """
    Retrieve a list of all authors.

    Returns:
        List[Author]: A list of all authors in the database.
    """
    return await list_items(Author)


async def get_author(item_id: int) -> Optional[Author]:
    """
    Retrieve a specific author by ID.

    Args:
        item_id (int): The ID of the author to retrieve.

    Returns:
        Optional[Author]: The retrieved author if found, otherwise None.
    """
    return await get_item(Author, item_id)


async def delete_author(item_id: int) -> None:
    """
    Delete a specific author by ID.

    Args:
        item_id (int): The ID of the author to delete.
    """
    await delete_item(Author, item_id)


async def update_author(item_id: int, update_data: dict) -> Optional[Author]:
    """
    Update an existing author by ID with new data.

    Args:
        item_id (int): The ID of the author to update.
        update_data (dict): A dictionary containing fields to update.

    Returns:
        Optional[Author]: The updated author instance if successful, otherwise None.
    """
    return await update_item(Author, item_id, update_data)
