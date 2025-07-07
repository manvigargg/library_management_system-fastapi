from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..schemas.author_schemas import AuthorCreate, AuthorUpdate, AuthorResponse
from ..services.library_service import LibraryService

authors_router = APIRouter(prefix="/authors", tags=["authors"])

def get_library_service():
    return LibraryService()

@authors_router.post("/", response_model=AuthorResponse)
async def create_author(
    author_data: AuthorCreate,
    service: LibraryService = Depends(get_library_service)
):
    """Create a new author"""
    try:
        author = service.create_author(
            name=author_data.name,
            biography=author_data.biography,
            birth_year=author_data.birth_year
        )
        return AuthorResponse(**author.to_dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@authors_router.get("/", response_model=List[AuthorResponse])
async def get_all_authors(service: LibraryService = Depends(get_library_service)):
    """Get all authors"""
    authors = service.get_all_authors()
    return [AuthorResponse(**author.to_dict()) for author in authors]

@authors_router.get("/{author_id}", response_model=AuthorResponse)
async def get_author(
    author_id: str,
    service: LibraryService = Depends(get_library_service)
):
    """Get author by ID"""
    author = service.get_author(author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return AuthorResponse(**author.to_dict())

@authors_router.put("/{author_id}", response_model=AuthorResponse)
async def update_author(
    author_id: str,
    author_data: AuthorUpdate,
    service: LibraryService = Depends(get_library_service)
):
    """Update author information"""
    try:
        update_dict = author_data.dict(exclude_unset=True)
        author = service.update_author(author_id, **update_dict)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        return AuthorResponse(**author.to_dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@authors_router.delete("/{author_id}")
async def delete_author(
    author_id: str,
    service: LibraryService = Depends(get_library_service)
):
    """Delete author"""
    try:
        if service.delete_author(author_id):
            return {"message": "Author deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Author not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))