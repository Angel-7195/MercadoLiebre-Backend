import uuid

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime

from app.database.base import Base

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True
    )
    email: Mapped[str] = mapped_column(
        Text,
        unique=True,
        nullable=False
    )
    password_hash: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="DISABLED_PASSWORD_HASH"
    )
    full_name: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    role: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        default="CLIENT")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    shopping = relationship(
        "Shopping",
        back_populates="user",
    )

    seller = relationship(
        "Seller",
        back_populates="user",
    )