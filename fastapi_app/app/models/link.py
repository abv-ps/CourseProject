from sqlmodel import SQLModel, Field


class AuthorBookLink(SQLModel, table=True):
    author_id: int = Field(foreign_key="authors.author_id", primary_key=True)
    book_id: int = Field(foreign_key="books.book_id", primary_key=True)
