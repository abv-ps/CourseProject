"""
Asynchronous CRUD utilities for SQLModel-based models with notification support.

This module provides generic asynchronous functions to create, retrieve, update,
delete, and list items in the database using SQLModel and an async session.
It also includes a simple notification function and a specific helper to fetch books
associated with authors.

Functions:
- send_notification: Log notification message on item creation.
- get_item: Fetch a single record by ID.
- delete_item: Remove a record by ID.
- list_items: Retrieve all records of a model.
- update_item: Update a record's fields by ID.
- get_author_books: Fetch books linked to one or multiple authors.
"""

from typing import Type, TypeVar, Optional, Any, List
from sqlmodel import SQLModel, select
from app.db.session import async_session

ModelType = TypeVar("ModelType", bound=SQLModel)


def send_notification(model: Type[SQLModel], item_name: str, item_id: int) -> None:
    """
    Simulate sending a notification when an item is created.

    Args:
        model (Type[SQLModel]): The model class.
        item_name (str): The name/title of the created item.
        item_id (int): The unique identifier of the created item.
    """
    print(
        f"{model.__name__} created: '{item_name}' (ID: {item_id}) → Notification sent."
    )


async def get_item(model: Type[ModelType], item_id: int) -> Optional[ModelType]:
    """
    Retrieve a single item by its ID.

    Args:
        model (Type[ModelType]): The model class to query.
        item_id (int): The ID of the item to retrieve.

    Returns:
        Optional[ModelType]: The item instance if found, else None.
    """
    async with async_session() as session:
        return await session.get(model, item_id)


async def delete_item(model: Type[ModelType], item_id: int) -> None:
    """
    Delete an item by its ID.

    Args:
        model (Type[ModelType]): The model class to query.
        item_id (int): The ID of the item to delete.
    """
    async with async_session() as session:
        item = await session.get(model, item_id)
        if item:
            await session.delete(item)
            await session.commit()


async def list_items(model: Type[ModelType]) -> List[ModelType]:
    """
    List all items of a given model.

    Args:
        model (Type[ModelType]): The model class to query.

    Returns:
        List[ModelType]: A list of all the items in the specified model.
    """
    async with async_session() as session:
        result = await session.execute(select(model))
        return result.scalars().all()


async def update_item(
    model: Type[ModelType], item_id: int, update_data: dict[str, Any]
) -> Optional[ModelType]:
    """
    Update fields of an item by its ID.

    Args:
        model (Type[ModelType]): The model class to query.
        item_id (int): The ID of the item to update.
        update_data (dict[str, Any]): A dictionary of fields to update.

    Returns:
        Optional[ModelType]: The updated item instance if found, else None.
    """
    async with async_session() as session:
        db_item = await session.get(model, item_id)
        if db_item:
            for key, value in update_data.items():
                setattr(db_item, key, value)
            session.add(db_item)
            await session.commit()
            await session.refresh(db_item)
        return db_item


async def get_author_books(
    author_id: Optional[int] = None,
    author_ids: Optional[List[int]] = None
) -> List["Book"]:
    """
    Retrieve books linked to one or multiple authors.

    Args:
        author_id (Optional[int]): A single author ID to filter by.
        author_ids (Optional[List[int]]): A list of author IDs to filter by.

    Returns:
        List[Book]: A list of Book instances related to the specified authors.
    """
    async with async_session() as session:
        from app.models.book import Book
        from app.models.author import AuthorBookLink

        author_book_query = select(Book).join(AuthorBookLink)

        if author_id is not None:
            author_book_query = author_book_query.where(AuthorBookLink.author_id == author_id)
        elif author_ids is not None:
            author_book_query = author_book_query.where(AuthorBookLink.author_id.in_(author_ids))

        result = await session.execute(author_book_query)
        return result.scalars().all()
