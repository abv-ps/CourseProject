from fastapi import APIRouter, BackgroundTasks, HTTPException
from typing import Optional

from app.crud.items import (get_item,
                            delete_item,
                            list_items,
                            update_item,
                            get_author_books
                            )
from app.crud.author import create_author
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorRead
from app.schemas.book import BookRead
from app.kafka.producer import kafka_producer

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.post("/", response_model=AuthorCreate)
async def create(author: AuthorCreate, background_tasks: BackgroundTasks):
    result = await create_author(Author(**author.model_dump()), background_tasks)
    await kafka_producer.send_event(
        key="author_created",
        payload={"author_id": result.author_id, "name": result.author_name}
    )
    return result

@router.get("/", response_model=list[AuthorRead])
async def list_all():
    return await list_items(Author)


@router.get("/{author_id}", response_model=AuthorRead)
async def get(author_id: int):
    author = await get_item(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.delete("/{author_id}")
async def delete(author_id: int):
    await delete_item(Author, author_id)
    return {"deleted": author_id}


@router.patch("/{author_id}", response_model=AuthorRead)
async def update(author_id: int, update_data: dict):
    updated = await update_item(Author, author_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Author not found")
    await kafka_producer.send_event(
        key="author_updated",
        payload={"author_id": updated.author_id, "name": updated.author_name}
    )
    return updated


@router.get("/{author_id}/books", response_model=list[BookRead])
async def get_books_by_author(author_id: int):
    return await get_author_books(author_id=author_id)


@router.get("/books")
async def get_books_by_multiple_authors(author_ids: Optional[list[int]] = None):
    return await get_author_books(author_ids=author_ids)
