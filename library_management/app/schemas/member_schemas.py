from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class MemberCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., pattern=r"[^@]+@[^@]+\.[^@]+")
    membership_id: str = Field(..., min_length=3)
    phone: Optional[str] = Field(None, min_length=7, max_length=15)

class MemberUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(None, pattern=r"[^@]+@[^@]+\.[^@]+")
    phone: Optional[str] = Field(None, min_length=7, max_length=15)

class MemberResponse(BaseModel):
    id: str
    name: str
    email: str
    membership_id: str
    phone: Optional[str]
    borrowed_books: List[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
