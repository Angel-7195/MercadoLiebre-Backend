from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.database.session import get_db
from app.models.sellers import Seller
from app.schemas.sellers import SellerCreate, SellerRead, SellerUpdate

router = APIRouter(prefix="/api/sellers", tags=["sellers"])


@router.get("", response_model=list[SellerRead])
async def list_sellers(db: AsyncSession = Depends(get_db)) -> list[Seller]:
    result = await db.execute(select(Seller).order_by(Seller.created_at.desc()))
    return list(result.scalars().all())


@router.get("/{seller_id}", response_model=SellerRead)
async def get_seller(
    seller_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Seller:
    seller = await db.get(Seller, seller_id)

    if not seller:
        raise NotFoundError("Seller not found")

    return seller


@router.post("", response_model=SellerRead, status_code=status.HTTP_201_CREATED)
async def create_seller(
    payload: SellerCreate,
    db: AsyncSession = Depends(get_db),
) -> Seller:
    seller = Seller(
        user_id=payload.user_id,
        document_number=payload.document_number,
        store_name=payload.store_name,
        phone=payload.phone,
    )

    db.add(seller)
    await db.commit()
    await db.refresh(seller)

    return seller


@router.put("/{seller_id}", response_model=SellerRead)
async def update_seller(
    seller_id: UUID,
    payload: SellerUpdate,
    db: AsyncSession = Depends(get_db),
) -> Seller:
    seller = await db.get(Seller, seller_id)

    if not seller:
        raise NotFoundError("Seller not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(seller, field, value)

    await db.commit()
    await db.refresh(seller)

    return seller


@router.delete("/{seller_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_seller(
    seller_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    seller = await db.get(Seller, seller_id)

    if not seller:
        raise NotFoundError("Seller not found")

    await db.delete(seller)
    await db.commit()