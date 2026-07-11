from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.database.session import get_db
from app.models.orders import Order
from app.schemas.orders import OrderCreate, OrderRead, OrderUpdate

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.get("", response_model=list[OrderRead])
async def list_orders(db: AsyncSession = Depends(get_db)) -> list[Order]:
    result = await db.execute(select(Order).order_by(Order.created_at.desc()))
    return list(result.scalars().all())


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(
    order_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Order:
    order = await db.get(Order, order_id)

    if not order:
        raise NotFoundError("Order not found")

    return order


@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(
    payload: OrderCreate,
    db: AsyncSession = Depends(get_db),
) -> Order:
    order = Order(
        user_id=payload.user_id,
        total_amount=payload.total_amount,
        status=payload.status,
    )

    db.add(order)
    await db.commit()
    await db.refresh(order)

    return order


@router.put("/{order_id}", response_model=OrderRead)
async def update_order(
    order_id: UUID,
    payload: OrderUpdate,
    db: AsyncSession = Depends(get_db),
) -> Order:
    order = await db.get(Order, order_id)

    if not order:
        raise NotFoundError("Order not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(order, field, value)

    await db.commit()
    await db.refresh(order)

    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    order_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    order = await db.get(Order, order_id)

    if not order:
        raise NotFoundError("Order not found")

    await db.delete(order)
    await db.commit()