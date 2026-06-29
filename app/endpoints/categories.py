from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.database.session import get_db
from app.models.categories import Category
from app.schemas.categories import (
    CategoryCreate,
    CategoryRead,
    CategoryUpdate,
)

router = APIRouter(
    prefix="/api/categories",
    tags=["categories"],
)


@router.get("", response_model=list[CategoryRead])
async def list_categories(
    db: AsyncSession = Depends(get_db),
) -> list[Category]:
    result = await db.execute(
        select(Category).order_by(Category.created_at.desc())
    )
    return list(result.scalars().all())


@router.get("/{category_id}", response_model=CategoryRead)
async def get_category(
    category_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Category:
    category = await db.get(Category, category_id)

    if not category:
        raise NotFoundError("Category not found")

    return category


@router.post("", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
    payload: CategoryCreate,
    db: AsyncSession = Depends(get_db),
) -> Category:
    category = Category(
        name=payload.name,
        description=payload.description,
    )

    db.add(category)
    await db.commit()
    await db.refresh(category)

    return category


@router.put("/{category_id}", response_model=CategoryRead)
async def update_category(
    category_id: UUID,
    payload: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
) -> Category:
    category = await db.get(Category, category_id)

    if not category:
        raise NotFoundError("Category not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(category, field, value)

    await db.commit()
    await db.refresh(category)

    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    category = await db.get(Category, category_id)

    if not category:
        raise NotFoundError("Category not found")

    await db.delete(category)
    await db.commit()