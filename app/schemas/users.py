from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1)
    role: str = Field(default="CLIENT")

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserUpdate(BaseModel):
    full_name: str | None = None
    password: str | None = None
    role: str | None = None

class UserRead(UserBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True