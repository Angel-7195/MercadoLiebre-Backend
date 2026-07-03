from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


# -----------------------------------------------------------------------------
# Esquema base para la entidad User.
# Contiene los campos comunes utilizados en varios esquemas.
# -----------------------------------------------------------------------------
class UserBase(BaseModel):
    # Correo electrónico del usuario.
    email: EmailStr

    # Nombre completo del usuario.
    full_name: str = Field(min_length=1)

    # Rol del usuario dentro de la aplicación.
    # Por defecto todos los usuarios son CLIENT.
    role: str = Field(default="CLIENT")


# -----------------------------------------------------------------------------
# Esquema utilizado para crear un nuevo usuario.
# Hereda los campos de UserBase y agrega la contraseña.
# -----------------------------------------------------------------------------
class UserCreate(UserBase):
    # La contraseña debe tener mínimo 8 caracteres.
    password: str = Field(min_length=8)


# -----------------------------------------------------------------------------
# Esquema utilizado para actualizar un usuario.
# Todos los campos son opcionales para permitir modificaciones parciales.
# -----------------------------------------------------------------------------
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    password: str | None = None
    role: str | None = None


# -----------------------------------------------------------------------------
# Esquema utilizado para devolver la información de un usuario.
# Incluye los campos generados automáticamente por la base de datos.
# -----------------------------------------------------------------------------
class UserRead(UserBase):
    # Identificador único del usuario.
    id: UUID

    # Fecha y hora en la que fue creado el usuario.
    created_at: datetime

    class Config:
        # Permite crear este esquema directamente a partir de un modelo ORM
        # de SQLAlchemy.
        from_attributes = True