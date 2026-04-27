from pydantic import BaseModel, EmailStr, constr
from enum import Enum
from typing import Optional
from app.core.enums import UserRole

class UserRequest(BaseModel):
    username: str
    email: EmailStr                 
    password: constr(min_length=6) 
    role: UserRole

class UserUpdateRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[constr(min_length=6)] = None
    role: Optional[UserRole] = None