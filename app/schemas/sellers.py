from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

class SellerBase(BaseModel):
    user_id: UUID
    document_number: str = Field(min_length=1, max_length=50)
    store_name: str = Field(min_length=1, max_length=100)
    phone: str | None = Field(default=None, max_length=30)

class SellerCreate(SellerBase):
    pass

class SellerUpdate(BaseModel):
    document_number: str | None = Field(default=None, min_length=1, max_length=50)
    store_name: str | None = Field(default=None, min_length=1, max_length=100)
    phone: str | None = Field(default=None, max_length=30)

class SellerRead(SellerBase):
    id: UUID
    rating: float
    created_at: datetime

    class Config:
        from_attributes = True