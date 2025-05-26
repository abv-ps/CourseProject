from typing import Optional
from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    description: Optional[str] = None


class BookCreate(BookBase):
    pass


class BookRead(BookBase):
    book_id: int

    class Config:
        orm_mode = True
