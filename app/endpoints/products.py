from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.database.session import get_db
from app.models.products import Product
from app.schemas.products import ProductCreate, ProductRead, ProductUpdate

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("", response_model=list[ProductRead])
async def list_products(
    db: AsyncSession = Depends(get_db),
) -> list[Product]:
    result = await db.execute(select(Product).order_by(Product.created_at.desc()))
    return list(result.scalars().all())


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(
    product_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Product:
    product = await db.get(Product, product_id)

    if not product:
        raise NotFoundError("Product not found")

    return product


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    payload: ProductCreate,
    db: AsyncSession = Depends(get_db),
) -> Product:
    product = Product(
        seller_id=payload.seller_id,
        category_id=payload.category_id,
        name=payload.name,
        description=payload.description,
        brand=payload.brand,
        price=payload.price,
        stock=payload.stock,
        status=payload.status,
        image_url=payload.image_url,
    )

    db.add(product)
    await db.commit()
    await db.refresh(product)

    return product


@router.put("/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: UUID,
    payload: ProductUpdate,
    db: AsyncSession = Depends(get_db),
) -> Product:
    product = await db.get(Product, product_id)

    if not product:
        raise NotFoundError("Product not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(product, field, value)

    await db.commit()
    await db.refresh(product)

    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    product = await db.get(Product, product_id)

    if not product:
        raise NotFoundError("Product not found")

    await db.delete(product)
    await db.commit()