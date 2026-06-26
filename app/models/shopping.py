import uuid

from sqlalchemy import DateTime, String, func, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal

from datetime import datetime

from app.database.base import Base

class Shopping(Base):
    __tablename__ = "shopping"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )
    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=0,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="Pending"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    user = relationship(
        "User",
        back_populates="shopping",
    )
    purchase_details = relationship(
        "PurchaseDetail",
        back_populates="shopping",
    )