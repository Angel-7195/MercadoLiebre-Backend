from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

class CategoryBase(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    description: str | None = Field(default=None, max_length=500)

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=80)
    description: str | None = Field(default=None, max_length=500)

class CategoryRead(CategoryBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True