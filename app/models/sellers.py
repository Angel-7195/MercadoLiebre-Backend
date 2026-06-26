import uuid

from sqlalchemy import DateTime, String, func, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime

from app.database.base import Base

class Seller(Base):
    __tablename__ = "seller"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        unique = True,
        nullable=False,
    )
    document_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )
    store_name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )
    phone: Mapped[str] = mapped_column(
        String(30),
        nullable=True,
    )
    rating: Mapped[float] = mapped_column(
        Numeric(3, 2),
        nullable=False,
        default=0,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user = relationship("User")