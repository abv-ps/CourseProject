"""
AuthorBookLink association table model for many-to-many relationship
between authors and books.

This module defines the AuthorBookLink class, which acts as a join table
linking authors and books via their respective primary keys.

Attributes:
    author_id (int): Foreign key referencing the authors table (primary key).
    book_id (int): Foreign key referencing the books table (primary key).
"""

from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field

class AuthorBookLink(SQLModel, table=True):
    author_id: int = Field(foreign_key="authors.author_id", primary_key=True)
    book_id: int = Field(foreign_key="books.book_id", primary_key=True)
