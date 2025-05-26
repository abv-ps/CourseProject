from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from app.models.link import AuthorBookLink

if TYPE_CHECKING:
    from app.models.book import Book



class Author(SQLModel, table=True):
    __tablename__ = 'authors'
    author_id: int = Field(default=None, primary_key=True)
    author_name: str

    books: list["Book"] = Relationship(back_populates="owners",
                                       link_model=AuthorBookLink,
                                       sa_relationship_kwargs={"lazy": "noload"}
                                       )
