from typing import Optional
from enum import Enum
from .base import BaseEntity

class BookStatus(Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"
    RESERVED = "reserved"
    MAINTENANCE = "maintenance"

class Book(BaseEntity):
    """Book entity demonstrating composition with Author"""
    
    def __init__(self, title: str, author_id: str, isbn: str, pages: int = 0, 
                 genre: Optional[str] = None):
        super().__init__(title)
        self._author_id: str = author_id
        self._isbn: str = isbn
        self._pages: int = pages
        self._genre: Optional[str] = genre
        self._status: BookStatus = BookStatus.AVAILABLE
        self._borrowed_by: Optional[str] = None  # Member ID
        self._borrowed_date: Optional[str] = None
    
    @property
    def author_id(self) -> str:
        return self._author_id
    
    @property
    def isbn(self) -> str:
        return self._isbn
    
    @isbn.setter
    def isbn(self, value: str):
        if not value or len(value) < 10:
            raise ValueError("ISBN must be at least 10 characters")
        self._isbn = value
    
    @property
    def pages(self) -> int:
        return self._pages
    
    @pages.setter
    def pages(self, value: int):
        if value < 0:
            raise ValueError("Pages cannot be negative")
        self._pages = value
    
    @property
    def status(self) -> BookStatus:
        return self._status
    
    @property
    def is_available(self) -> bool:
        return self._status == BookStatus.AVAILABLE
    
    def borrow(self, member_id: str) -> bool:
        """Borrow the book to a member"""
        if self.is_available:
            self._status = BookStatus.BORROWED
            self._borrowed_by = member_id
            from datetime import datetime
            self._borrowed_date = datetime.now().isoformat()
            return True
        return False
    
    def return_book(self) -> bool:
        """Return the book"""
        if self._status == BookStatus.BORROWED:
            self._status = BookStatus.AVAILABLE
            self._borrowed_by = None
            self._borrowed_date = None
            return True
        return False
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.name,
            "author_id": self.author_id,
            "isbn": self.isbn,
            "pages": self.pages,
            "genre": self._genre,
            "status": self.status.value,
            "borrowed_by": self._borrowed_by,
            "borrowed_date": self._borrowed_date,
            "created_at": self._created_at.isoformat(),
            "updated_at": self._updated_at.isoformat()
        }