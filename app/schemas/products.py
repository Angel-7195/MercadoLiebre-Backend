from datetime import datetime
from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    category_id: UUID
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    brand: str | None = Field(default=None, max_length=50)
    price: Decimal = Field(gt=0)
    stock: int = Field(ge=0)

class ProductCreate(ProductBase):
    image_url: str | None = Field(
        default=None,
        max_length=200
    )

class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    brand: str | None = Field(default=None, max_length=50)
    price: Decimal | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
    category_id: UUID | None = None
    status: str | None = Field(default=None, max_length=20)
    image_url: str | None = Field(default=None, max_length=500)

class ProductRead(ProductBase):
    id: UUID
    seller_id: UUID
    status: str = Field(max_length=20)
    image_url: str | None = Field(default=None, max_length=500)
    created_at: datetime

    class Config:
        from_attributes = True