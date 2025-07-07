from typing import Optional
from .base import BaseEntity
from ..services.library_service import LibraryService

class Member(BaseEntity):
    """Member entity representing a library user"""

    def __init__(self, name: str, email: str, membership_id: str, phone: Optional[str] = None):
        super().__init__(name)
        self._email: str = email
        self._membership_id: str = membership_id
        self._phone: Optional[str] = phone
        self._borrowed_books: list[str] = []

    @property
    def email(self) -> str:
        return self._email

    @property
    def membership_id(self) -> str:
        return self._membership_id

    @property
    def phone(self) -> Optional[str]:
        return self._phone

    @property
    def borrowed_books(self) -> list[str]:
        return self._borrowed_books

    def borrow_book(self, book_id: str):
        if book_id not in self._borrowed_books:
            self._borrowed_books.append(book_id)

    def return_book(self, book_id: str):
        if book_id in self._borrowed_books:
            self._borrowed_books.remove(book_id)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "membership_id": self.membership_id,
            "phone": self.phone,
            "borrowed_books": self.borrowed_books,
            "created_at": self._created_at.isoformat(),
            "updated_at": self._updated_at.isoformat()
        }
