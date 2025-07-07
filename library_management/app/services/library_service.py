from typing import List, Optional, Dict, Any
from ..models.author import Author
from ..models.book import Book, BookStatus
from ..models.member import Member
from .data_storage import DataStorage

class LibraryService:
    """Main business logic service demonstrating composition and error handling"""
    
    def __init__(self):
        self.storage = DataStorage()
    
    # Author operations
    def create_author(self, name: str, biography: Optional[str] = None, 
                     birth_year: Optional[int] = None) -> Author:
        """Create a new author"""
        try:
            author = Author(name, biography, birth_year)
            data = self.storage.load_data()
            data["authors"][author.id] = author.to_dict()
            self.storage.save_data(data)
            return author
        except Exception as e:
            raise RuntimeError(f"Failed to create author: {e}")
    
    def get_author(self, author_id: str) -> Optional[Author]:
        """Get author by ID"""
        data = self.storage.load_data()
        author_data = data["authors"].get(author_id)
        if author_data:
            author = Author(author_data["name"], author_data.get("biography"), 
                          author_data.get("birth_year"))
            author._id = author_data["id"]
            return author
        return None
    
    def get_all_authors(self) -> List[Author]:
        """Get all authors"""
        data = self.storage.load_data()
        authors = []
        for author_data in data["authors"].values():
            author = Author(author_data["name"], author_data.get("biography"),
                          author_data.get("birth_year"))
            author._id = author_data["id"]
            authors.append(author)
        return authors
    
    def update_author(self, author_id: str, **kwargs) -> Optional[Author]:
        """Update author information"""
        author = self.get_author(author_id)
        if not author:
            return None
        
        try:
            if "name" in kwargs:
                author.name = kwargs["name"]
            if "biography" in kwargs:
                author.biography = kwargs["biography"]
            if "birth_year" in kwargs:
                author.birth_year = kwargs["birth_year"]
            
            data = self.storage.load_data()
            data["authors"][author_id] = author.to_dict()
            self.storage.save_data(data)
            return author
        except Exception as e:
            raise RuntimeError(f"Failed to update author: {e}")
    
    def delete_author(self, author_id: str) -> bool:
        """Delete author (only if no books associated)"""
        data = self.storage.load_data()
        if author_id not in data["authors"]:
            return False
        
        # Check if author has books
        author_books = [book for book in data["books"].values() 
                       if book["author_id"] == author_id]
        if author_books:
            raise ValueError("Cannot delete author with associated books")
        
        del data["authors"][author_id]
        self.storage.save_data(data)
        return True
    
    # Book operations
    def create_book(self, title: str, author_id: str, isbn: str, 
                   pages: int = 0, genre: Optional[str] = None) -> Book:
        """Create a new book"""
        # Verify author exists
        if not self.get_author(author_id):
            raise ValueError("Author not found")
        
        try:
            book = Book(title, author_id, isbn, pages, genre)
            data = self.storage.load_data()
            data["books"][book.id] = book.to_dict()
            
            # Update author's book list
            data["authors"][author_id]["books"].append(book.id)
            
            self.storage.save_data(data)
            return book
        except Exception as e:
            raise RuntimeError(f"Failed to create book: {e}")
    
    def get_book(self, book_id: str) -> Optional[Book]:
        """Get book by ID"""
        data = self.storage.load_data()
        book_data = data["books"].get(book_id)
        if book_data:
            book = Book(book_data["title"], book_data["author_id"], 
                       book_data["isbn"], book_data["pages"], book_data.get("genre"))
            book._id = book_data["id"]
            book._status = BookStatus(book_data["status"])
            book._borrowed_by = book_data.get("borrowed_by")
            book._borrowed_date = book_data.get("borrowed_date")
            return book
        return None
    
    def search_books(self, query: str) -> List[Book]:
        """Search books by title, author name, or genre"""
        data = self.storage.load_data()
        results = []
        query = query.lower()
        
        for book_data in data["books"].values():
            # Search in title
            if query in book_data["title"].lower():
                results.append(self._dict_to_book(book_data))
                continue
            
            # Search in author name
            author_data = data["authors"].get(book_data["author_id"])
            if author_data and query in author_data["name"].lower():
                results.append(self._dict_to_book(book_data))
                continue
            
            # Search in genre
            genre = book_data.get("genre", "")
            if genre and query in genre.lower():
                results.append(self._dict_to_book(book_data))
        
        return results
    
    def _dict_to_book(self, book_data: Dict) -> Book:
        """Helper method to convert dict to Book object"""
        book = Book(book_data["title"], book_data["author_id"], 
                   book_data["isbn"], book_data["pages"], book_data.get("genre"))
        book._id = book_data["id"]
        book._status = BookStatus(book_data["status"])
        book._borrowed_by = book_data.get("borrowed_by")
        book._borrowed_date = book_data.get("borrowed_date")
        return book
    
    # Member operations
    def create_member(self, name: str, email: str, phone: Optional[str] = None) -> Member:
        """Create a new member"""
        try:
            member = Member(name, email, phone)
            data = self.storage.load_data()
            data["members"][member.id] = member.to_dict()
            self.storage.save_data(data)
            return member
        except Exception as e:
            raise RuntimeError(f"Failed to create member: {e}")
    
    def get_member(self, member_id: str) -> Optional[Member]:
        """Get member by ID"""
        data = self.storage.load_data()
        member_data = data["members"].get(member_id)
        if member_data:
            member = Member(member_data["name"], member_data["email"], 
                          member_data.get("phone"))
            member._id = member_data["id"]
            member._borrowed_books = member_data.get("borrowed_books", [])
            return member
        return None
    
    # Borrowing operations
    def borrow_book(self, book_id: str, member_id: str) -> bool:
        """Handle book borrowing transaction"""
        book = self.get_book(book_id)
        member = self.get_member(member_id)
        
        if not book or not member:
            raise ValueError("Book or member not found")
        
        if not book.is_available:
            raise ValueError("Book is not available")
        
        if not member.can_borrow:
            raise ValueError("Member has reached borrowing limit")
        
        # Perform borrowing transaction
        if book.borrow(member_id) and member.borrow_book(book_id):
            data = self.storage.load_data()
            data["books"][book_id] = book.to_dict()
            data["members"][member_id] = member.to_dict()
            self.storage.save_data(data)
            return True
        
        return False
    
    def return_book(self, book_id: str, member_id: str) -> bool:
        """Handle book return transaction"""
        book = self.get_book(book_id)
        member = self.get_member(member_id)
        
        if not book or not member:
            raise ValueError("Book or member not found")
        
        if book._borrowed_by != member_id:
            raise ValueError("Book not borrowed by this member")
        
        # Perform return transaction
        if book.return_book() and member.return_book(book_id):
            data = self.storage.load_data()
            data["books"][book_id] = book.to_dict()
            data["members"][member_id] = member.to_dict()
            self.storage.save_data(data)
            return True
        
        return False
