from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class PurchaseDetailBase(BaseModel):
    shopping_id: UUID
    product_id: UUID
    quantity: int = Field(ge=1)
    unit_price: Decimal = Field(gt=0)
    subtotal: Decimal = Field(ge=0)


class PurchaseDetailCreate(PurchaseDetailBase):
    pass


class PurchaseDetailUpdate(BaseModel):
    quantity: int | None = Field(default=None, ge=1)
    unit_price: Decimal | None = Field(default=None, gt=0)
    subtotal: Decimal | None = Field(default=None, ge=0)


class PurchaseDetailRead(PurchaseDetailBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True