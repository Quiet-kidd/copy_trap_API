from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str
    
class UserCreate(BaseModel):
    name: str
    phone_number: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    name: str
    phone_number: str
    email: EmailStr
    id: int
    created_at: datetime
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class ReportCreate(BaseModel):
    # matched_sources: Optional[str] = None
    payload: dict
    status: str
    document_id: int
    
class ReportOut(ReportCreate):
    id: int
    created_at: datetime
    
class TokenData(BaseModel):
    id: Optional[int] = None
    
class DocumentCreate(BaseModel):
    user_id : int
    title: str
    content: str
    
class DocumentOut(DocumentCreate):
    id: int
    created_at: datetime

class LoginOut(Token):
    user: UserOut
    