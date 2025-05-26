"""
Book model representing books with relationships to authors.

This module defines the SQLModel-based Book class for database interaction,
including an optional description field and a many-to-many relationship
to authors via the AuthorBookLink association table.

Attributes:
    book_id (int): Primary key identifier for the book.
    title (str): Title of the book.
    description (Optional[str]): Optional textual description of the book.
    owners (List[Author]): Related authors linked through AuthorBookLink.

The relationship uses lazy loading with the 'noload' strategy to optimize query performance.
"""

from typing import Optional, TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Relationship
from app.models.link import AuthorBookLink

if TYPE_CHECKING:
    from app.models.author import Author


class Book(SQLModel, table=True):
    __tablename__ = "books"

    book_id: int = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None

    owners: List["Author"] = Relationship(
        back_populates="books",
        link_model=AuthorBookLink,
        sa_relationship_kwargs={"lazy": "noload"},
    )
