from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

class OrderBase(BaseModel):
    user_id: UUID
    total_amount: Decimal = Field(default=0)
    status: str = Field(default="PENDING")

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    total_amount: Decimal | None = None
    status: str | None = None

class OrderRead(OrderBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True