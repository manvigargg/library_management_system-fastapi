from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class BookStatus(str, Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"
    RESERVED = "reserved"
    MAINTENANCE = "maintenance"

class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author_id: str
    isbn: str = Field(..., min_length=10, max_length=17)
    pages: int = Field(0, ge=0)
    genre: Optional[str] = Field(None, max_length=50)

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    isbn: Optional[str] = Field(None, min_length=10, max_length=17)
    pages: Optional[int] = Field(None, ge=0)
    genre: Optional[str] = Field(None, max_length=50)

class BookResponse(BaseModel):
    id: str
    title: str
    author_id: str
    isbn: str
    pages: int
    genre: Optional[str] = None
    status: BookStatus
    borrowed_by: Optional[str] = None
    borrowed_date: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class BorrowRequest(BaseModel):
    member_id: str