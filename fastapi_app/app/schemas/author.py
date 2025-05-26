"""
Pydantic schemas for author data validation and serialization.

This module defines base, create, and read schemas for authors,
including support for nested related books.

Schemas:
- AuthorBase: Shared properties for author data.
- AuthorCreate: Schema for creating a new author.
- AuthorRead: Schema for reading author data, including related books.
"""

from typing import List, Optional
from pydantic import BaseModel
from app.schemas.book import BookRead


class AuthorBase(BaseModel):
    """Base schema with common author attributes."""
    author_name: str


class AuthorCreate(AuthorBase):
    """Schema for author creation (inherits from AuthorBase)."""
    pass


class AuthorRead(AuthorBase):
    """Schema for reading author data, including related books."""
    author_id: int
    books: Optional[List[BookRead]] = []

    class Config:
        orm_mode = True
