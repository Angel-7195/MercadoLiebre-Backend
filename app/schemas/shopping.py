from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

class ShoppingBase(BaseModel):
    user_id: UUID
    total_amount: Decimal = Field(default=0)
    status: str = Field(default="PENDING")

class ShoppingCreate(ShoppingBase):
    pass

class ShoppingUpdate(BaseModel):
    total_amount: Decimal | None = None
    status: str | None = None

class ShoppingRead(ShoppingBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True