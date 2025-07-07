from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class AuthorCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    biography: Optional[str] = Field(None, max_length=1000)
    birth_year: Optional[int] = Field(None, ge=1800, le=2024)

class AuthorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    biography: Optional[str] = Field(None, max_length=1000)
    birth_year: Optional[int] = Field(None, ge=1800, le=2024)

class AuthorResponse(BaseModel):
    id: str
    name: str
    biography: Optional[str] = None
    birth_year: Optional[int] = None
    books: List[str] = []
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
