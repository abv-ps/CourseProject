"""
Pydantic schemas for book data validation and serialization.

This module provides base, create, and read schemas for book entities,
enabling structured input validation and output formatting.

Schemas:
- BookBase: Common fields for book data.
- BookCreate: Schema for creating a new book.
- BookRead: Schema for reading book data with ID included.
"""

from typing import Optional
from pydantic import BaseModel


class BookBase(BaseModel):
    """Base schema with common book attributes."""
    title: str
    description: Optional[str] = None


class BookCreate(BookBase):
    """Schema for book creation (inherits from BookBase)."""
    pass


class BookRead(BookBase):
    """Schema for reading book data, including book ID."""
    book_id: int

    class Config:
        orm_mode = True
