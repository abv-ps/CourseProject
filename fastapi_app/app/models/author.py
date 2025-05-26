"""
Author model representing authors with relationships to books.

Defines the SQLModel-based Author class for database interaction, including
a many-to-many relationship to books via an association table AuthorBookLink.

Attributes:
    author_id (int): Primary key for the author.
    author_name (str): Name of the author.
    books (List[Book]): Related books linked through AuthorBookLink association.

This model uses lazy loading with 'noload' strategy for the 'books' relationship
to optimize query performance.
"""

from typing import TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Relationship
from app.models.link import AuthorBookLink

if TYPE_CHECKING:
    from app.models.book import Book


class Author(SQLModel, table=True):
    __tablename__ = "authors"

    author_id: int = Field(default=None, primary_key=True)
    author_name: str

    books: List["Book"] = Relationship(
        back_populates="owners",
        link_model=AuthorBookLink,
        sa_relationship_kwargs={"lazy": "noload"},
    )
