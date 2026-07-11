from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.database.session import get_db
from app.models.purchase_details import PurchaseDetail
from app.schemas.purchase_details import (
    PurchaseDetailCreate,
    PurchaseDetailRead,
    PurchaseDetailUpdate,
)

router = APIRouter(
    prefix="/api/purchase_details",
    tags=["purchase_details"],
)


@router.get("", response_model=list[PurchaseDetailRead])
async def list_purchase_details(
    db: AsyncSession = Depends(get_db),
) -> list[PurchaseDetail]:
    result = await db.execute(
        select(PurchaseDetail).order_by(PurchaseDetail.created_at.desc())
    )
    return list(result.scalars().all())


@router.get("/{purchase_detail_id}", response_model=PurchaseDetailRead)
async def get_purchase_detail(
    purchase_detail_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> PurchaseDetail:
    purchase_detail = await db.get(PurchaseDetail, purchase_detail_id)

    if not purchase_detail:
        raise NotFoundError("Purchase detail not found")

    return purchase_detail


@router.post("", response_model=PurchaseDetailRead, status_code=status.HTTP_201_CREATED)
async def create_purchase_detail(
    payload: PurchaseDetailCreate,
    db: AsyncSession = Depends(get_db),
) -> PurchaseDetail:
    purchase_detail = PurchaseDetail(
        order_id=payload.order_id,
        product_id=payload.product_id,
        quantity=payload.quantity,
        unit_price=payload.unit_price,
        subtotal=payload.subtotal,
    )

    db.add(purchase_detail)
    await db.commit()
    await db.refresh(purchase_detail)

    return purchase_detail


@router.put("/{purchase_detail_id}", response_model=PurchaseDetailRead)
async def update_purchase_detail(
    purchase_detail_id: UUID,
    payload: PurchaseDetailUpdate,
    db: AsyncSession = Depends(get_db),
) -> PurchaseDetail:
    purchase_detail = await db.get(PurchaseDetail, purchase_detail_id)

    if not purchase_detail:
        raise NotFoundError("Purchase detail not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(purchase_detail, field, value)

    await db.commit()
    await db.refresh(purchase_detail)

    return purchase_detail


@router.delete("/{purchase_detail_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_purchase_detail(
    purchase_detail_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    purchase_detail = await db.get(PurchaseDetail, purchase_detail_id)

    if not purchase_detail:
        raise NotFoundError("Purchase detail not found")

    await db.delete(purchase_detail)
    await db.commit()