import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


# -----------------------------------------------------------------------------
# Modelo User
#
# Representa a los usuarios registrados en MercadoLiebre.
# Cada usuario puede actuar como cliente (CLIENT) o administrador (ADMIN).
#
# Esta clase se convierte automáticamente en la tabla "users" de PostgreSQL
# mediante SQLAlchemy.
# -----------------------------------------------------------------------------
class User(Base):
    # Nombre de la tabla en la base de datos.
    __tablename__ = "users"

    # -------------------------------------------------------------------------
    # Llave primaria (UUID generado automáticamente).
    # Identifica de forma única a cada usuario.
    # -------------------------------------------------------------------------
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
    )

    # -------------------------------------------------------------------------
    # Correo electrónico del usuario.
    # Debe ser único para evitar cuentas duplicadas.
    # -------------------------------------------------------------------------
    email: Mapped[str] = mapped_column(
        Text,
        unique=True,
        nullable=False,
    )

    # -------------------------------------------------------------------------
    # Contraseña almacenada en forma de hash.
    # Nunca se guarda la contraseña en texto plano.
    # -------------------------------------------------------------------------
    password_hash: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="DISABLED_PASSWORD_HASH",
    )

    # -------------------------------------------------------------------------
    # Nombre completo del usuario.
    # -------------------------------------------------------------------------
    full_name: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # -------------------------------------------------------------------------
    # Rol del usuario dentro del sistema.
    # Valores posibles:
    #   - CLIENT
    #   - ADMIN
    # -------------------------------------------------------------------------
    role: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        default="CLIENT",
    )

    # -------------------------------------------------------------------------
    # Fecha y hora en que se creó el usuario.
    # Se genera automáticamente utilizando la hora del servidor.
    # -------------------------------------------------------------------------
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    # ========================= RELACIONES =========================

    # -------------------------------------------------------------------------
    # Relación uno a muchos:
    # Un usuario puede realizar múltiples compras.
    # -------------------------------------------------------------------------
    orders = relationship(
        "Order",
        back_populates="user",
    )

    # -------------------------------------------------------------------------
    # Relación uno a uno:
    # Un usuario puede tener un único perfil de vendedor.
    # (Solo si decide vender productos en MercadoLiebre).
    # -------------------------------------------------------------------------
    seller = relationship(
        "Seller",
        back_populates="user",
    )