from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.core.security import get_current_user
from app.database.session import get_db
from app.models.sellers import Seller
from app.models.users import User
from app.schemas.sellers import SellerCreate, SellerRead, SellerUpdate

router = APIRouter(prefix="/api/sellers", tags=["sellers"])


@router.get("", response_model=list[SellerRead])
async def list_sellers(
    db: AsyncSession = Depends(get_db),
) -> list[Seller]:

    result = await db.execute(
        select(Seller).order_by(Seller.created_at.desc())
    )

    return list(result.scalars().all())


@router.post("", response_model=SellerRead, status_code=status.HTTP_201_CREATED)
async def create_seller(
    payload: SellerCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Seller:

    existing_seller = await db.execute(
        select(Seller).where(Seller.user_id == current_user.id)
    )

    if existing_seller.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already has a seller profile",
        )

    seller = Seller(
        user_id=current_user.id,
        document_number=payload.document_number,
        store_name=payload.store_name,
        phone=payload.phone,
    )

    db.add(seller)
    await db.commit()
    await db.refresh(seller)

    return seller


# Obtiene el perfil del vendedor autenticado.
@router.get("/me", response_model=SellerRead)
async def get_my_seller(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Seller:

    result = await db.execute(
        select(Seller).where(Seller.user_id == current_user.id)
    )

    seller = result.scalar_one_or_none()

    if not seller:
        raise NotFoundError("Seller profile not found")

    return seller


# Actualiza el perfil del vendedor autenticado.
@router.put("/me", response_model=SellerRead)
async def update_my_seller(
    payload: SellerUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Seller:

    result = await db.execute(
        select(Seller).where(Seller.user_id == current_user.id)
    )

    seller = result.scalar_one_or_none()

    if not seller:
        raise NotFoundError("Seller profile not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(seller, field, value)

    await db.commit()
    await db.refresh(seller)

    return seller


@router.get("/{seller_id}", response_model=SellerRead)
async def get_seller(
    seller_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Seller:

    seller = await db.get(Seller, seller_id)

    if not seller:
        raise NotFoundError("Seller not found")

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