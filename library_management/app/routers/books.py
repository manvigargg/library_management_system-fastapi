from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from ..schemas.book_schemas import BookCreate, BookUpdate, BookResponse, BorrowRequest
from ..services.library_service import LibraryService

# Create router for book-related endpoints
books_router = APIRouter(prefix="/books", tags=["books"])

# Dependency to get LibraryService instance
def get_library_service():
    return LibraryService()


# 1. Create a new book
@books_router.post("/", response_model=BookResponse)
async def create_book(
    book_data: BookCreate,
    service: LibraryService = Depends(get_library_service)
):
    """Create a new book"""
    try:
        book = service.create_book(
            title=book_data.title,
            author_id=book_data.author_id,
            isbn=book_data.isbn,
            pages=book_data.pages,
            genre=book_data.genre
        )
        return BookResponse(**book.to_dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# 2. Search books by title, author, or genre
@books_router.get("/search", response_model=List[BookResponse])
async def search_books(
    q: str = Query(..., description="Search query"),
    service: LibraryService = Depends(get_library_service)
):
    """Search books by title, author, or genre"""
    books = service.search_books(q)
    return [BookResponse(**book.to_dict()) for book in books]


# 3. Get a book by ID
@books_router.get("/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: str,
    service: LibraryService = Depends(get_library_service)
):
    """Get book by ID"""
    book = service.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookResponse(**book.to_dict())


# 4. Borrow a book
@books_router.post("/{book_id}/borrow")
async def borrow_book(
    book_id: str,
    borrow_data: BorrowRequest,
    service: LibraryService = Depends(get_library_service)
):
    """Borrow a book"""
    try:
        if service.borrow_book(book_id, borrow_data.member_id):
            return {"message": "Book borrowed successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to borrow book")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# 5. Return a book
@books_router.post("/{book_id}/return")
async def return_book(
    book_id: str,
    return_data: BorrowRequest,
    service: LibraryService = Depends(get_library_service)
):
    """Return a borrowed book"""
    try:
        if service.return_book(book_id, return_data.member_id):
            return {"message": "Book returned successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to return book")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# 6. Update book information
@books_router.put("/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: str,
    book_data: BookUpdate,
    service: LibraryService = Depends(get_library_service)
):
    """Update book information"""
    try:
        update_dict = book_data.dict(exclude_unset=True)
        book = service.update_book(book_id, **update_dict)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return BookResponse(**book.to_dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
