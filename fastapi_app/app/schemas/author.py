from typing import List, Optional
from pydantic import BaseModel
from app.schemas.book import BookRead


class AuthorBase(BaseModel):
    author_name: str


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    author_id: int
    books: Optional[List[BookRead]] = []

    class Config:
        orm_mode = True
