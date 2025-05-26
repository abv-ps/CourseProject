from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from app.models.link import AuthorBookLink

if TYPE_CHECKING:
    from app.models.author import Author


class Book(SQLModel, table=True):
    __tablename__ = 'books'
    book_id: int = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None

    owners: list["Author"] = Relationship(back_populates="books",
                                          link_model=AuthorBookLink,
                                          sa_relationship_kwargs={"lazy": "noload"}
                                          )
