from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..schemas.member_schemas import MemberCreate, MemberUpdate, MemberResponse
from ..services.library_service import LibraryService

members_router = APIRouter(prefix="/members", tags=["members"])

def get_library_service():
    return LibraryService()

@members_router.post("/", response_model=MemberResponse)
async def create_member(
    member_data: MemberCreate,
    service: LibraryService = Depends(get_library_service)
):
    """Create a new member"""
    try:
        member = service.create_member(
            name=member_data.name,
            email=member_data.email,
            phone=member_data.phone
        )
        return MemberResponse(**member.to_dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@members_router.get("/", response_model=List[MemberResponse])
async def get_all_members(service: LibraryService = Depends(get_library_service)):
    """Get all members"""
    members = service.get_all_members()
    return [MemberResponse(**member.to_dict()) for member in members]

@members_router.get("/{member_id}", response_model=MemberResponse)
async def get_member(
    member_id: str,
    service: LibraryService = Depends(get_library_service)
):
    """Get member by ID"""
    member = service.get_member(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return MemberResponse(**member.to_dict())

@members_router.put("/{member_id}", response_model=MemberResponse)
async def update_member(
    member_id: str,
    member_data: MemberUpdate,
    service: LibraryService = Depends(get_library_service)
):
    """Update member information"""
    try:
        update_dict = member_data.dict(exclude_unset=True)
        member = service.update_member(member_id, **update_dict)
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        return MemberResponse(**member.to_dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@members_router.delete("/{member_id}")
async def delete_member(
    member_id: str,
    service: LibraryService = Depends(get_library_service)
):
    """Delete member"""
    try:
        if service.delete_member(member_id):
            return {"message": "Member deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Member not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@members_router.get("/{member_id}/borrowed-books", response_model=List[dict])
async def get_member_borrowed_books(
    member_id: str,
    service: LibraryService = Depends(get_library_service)
):
    """Get books borrowed by a member"""
    try:
        books = service.get_member_borrowed_books(member_id)
        return [book.to_dict() for book in books]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
