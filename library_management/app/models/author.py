from typing import List, Optional
from .base import BaseEntity

class Author(BaseEntity):
    """Author entity with composition relationship to books"""
    
    def __init__(self, name: str, biography: Optional[str] = None, birth_year: Optional[int] = None):
        super().__init__(name)
        self._biography: Optional[str] = biography
        self._birth_year: Optional[int] = birth_year
        self._books: List[str] = []  # List of book IDs
    
    @property
    def biography(self) -> Optional[str]:
        return self._biography
    
    @biography.setter
    def biography(self, value: Optional[str]):
        self._biography = value.strip() if value else None
    
    @property
    def birth_year(self) -> Optional[int]:
        return self._birth_year
    
    @birth_year.setter
    def birth_year(self, value: Optional[int]):
        if value and (value < 1800 or value > 2024):
            raise ValueError("Birth year must be between 1800 and 2024")
        self._birth_year = value
    
    @property
    def books(self) -> List[str]:
        return self._books.copy()  # Return copy to maintain encapsulation
    
    def add_book(self, book_id: str):
        """Add a book to author's book list"""
        if book_id not in self._books:
            self._books.append(book_id)
    
    def remove_book(self, book_id: str):
        """Remove a book from author's book list"""
        if book_id in self._books:
            self._books.remove(book_id)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "biography": self.biography,
            "birth_year": self.birth_year,
            "books": self.books,
            "created_at": self._created_at.isoformat(),
            "updated_at": self._updated_at.isoformat()
        }
