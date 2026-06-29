from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.database.session import get_db
from app.models.shopping import Shopping
from app.schemas.shopping import ShoppingCreate, ShoppingRead, ShoppingUpdate

router = APIRouter(prefix="/api/shopping", tags=["shopping"])


@router.get("", response_model=list[ShoppingRead])
async def list_shopping(db: AsyncSession = Depends(get_db)) -> list[Shopping]:
    result = await db.execute(select(Shopping).order_by(Shopping.created_at.desc()))
    return list(result.scalars().all())


@router.get("/{shopping_id}", response_model=ShoppingRead)
async def get_shopping(
    shopping_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Shopping:
    shopping = await db.get(Shopping, shopping_id)

    if not shopping:
        raise NotFoundError("Shopping not found")

    return shopping


@router.post("", response_model=ShoppingRead, status_code=status.HTTP_201_CREATED)
async def create_shopping(
    payload: ShoppingCreate,
    db: AsyncSession = Depends(get_db),
) -> Shopping:
    shopping = Shopping(
        user_id=payload.user_id,
        total_amount=payload.total_amount,
        status=payload.status,
    )

    db.add(shopping)
    await db.commit()
    await db.refresh(shopping)

    return shopping


@router.put("/{shopping_id}", response_model=ShoppingRead)
async def update_shopping(
    shopping_id: UUID,
    payload: ShoppingUpdate,
    db: AsyncSession = Depends(get_db),
) -> Shopping:
    shopping = await db.get(Shopping, shopping_id)

    if not shopping:
        raise NotFoundError("Shopping not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(shopping, field, value)

    await db.commit()
    await db.refresh(shopping)

    return shopping


@router.delete("/{shopping_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shopping(
    shopping_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    shopping = await db.get(Shopping, shopping_id)

    if not shopping:
        raise NotFoundError("Shopping not found")

    await db.delete(shopping)
    await db.commit()