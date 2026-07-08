from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.core.security import hash_password
from app.database.session import get_db
from app.models.users import User
from app.schemas.users import UserCreate, UserRead, UserUpdate

# -----------------------------------------------------------------------------
# Router de FastAPI para la entidad Users.
# Todas las rutas de este archivo comenzarán con "/api/users".
# -----------------------------------------------------------------------------
router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)


# -----------------------------------------------------------------------------
# GET /api/users
# Obtiene la lista completa de usuarios registrados en la base de datos.
# Los usuarios se muestran ordenados desde el más reciente al más antiguo.
# -----------------------------------------------------------------------------
@router.get("", response_model=list[UserRead])
async def list_users(db: AsyncSession = Depends(get_db)) -> list[User]:
    result = await db.execute(
        select(User).order_by(User.created_at.desc())
    )
    return list(result.scalars().all())


# -----------------------------------------------------------------------------
# GET /api/users/{user_id}
# Busca un usuario por su identificador UUID.
# Si no existe, lanza una excepción personalizada 404.
# -----------------------------------------------------------------------------
@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> User:

    user = await db.get(User, user_id)

    if not user:
        raise NotFoundError("User not found")

    return user


# -----------------------------------------------------------------------------
# POST /api/users
# Crea un nuevo usuario.
#
# Antes de guardarlo:
# - Verifica que el correo electrónico no exista.
# - Encripta la contraseña utilizando bcrypt.
# - Guarda el usuario en la base de datos.
# -----------------------------------------------------------------------------
@router.post(
    "",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> User:

    # Verificar si ya existe un usuario con el mismo correo.
    existing = await db.execute(
        select(User).where(User.email == payload.email)
    )

    if existing.scalar_one_or_none() is not None:
        raise ConflictError("Email already exists")

    # Crear el nuevo objeto User.
    user = User(
        email=payload.email,
        full_name=payload.full_name,
        role=payload.role or "CLIENT",
        password_hash=hash_password(payload.password),
    )

    # Guardar el usuario en la base de datos.
    db.add(user)
    await db.commit()

    # Recargar el objeto para obtener datos generados automáticamente,
    # como el UUID y la fecha de creación.
    await db.refresh(user)

    return user


# -----------------------------------------------------------------------------
# PUT /api/users/{user_id}
# Actualiza los datos de un usuario existente.
#
# Solo modifica los campos enviados por el cliente.
# -----------------------------------------------------------------------------
@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: UUID,
    payload: UserUpdate,
    db: AsyncSession = Depends(get_db),
) -> User:

    user = await db.get(User, user_id)

    if not user:
        raise NotFoundError("User not found")

    # Si el correo cambia, validar que siga siendo único.
    if payload.email is not None:

        existing = await db.execute(
            select(User).where(
                User.email == payload.email,
                User.id != user_id,
            )
        )

        if existing.scalar_one_or_none() is not None:
            raise ConflictError("Email already exists")

        user.email = payload.email

    # Actualizar nombre completo.
    if payload.full_name is not None:
        user.full_name = payload.full_name

    # Actualizar contraseña.
    # La contraseña se cifra antes de guardarse en la base de datos.
    if payload.password is not None:
        user.password_hash = hash_password(payload.password)

    # Actualizar rol.
    if payload.role is not None:
        user.role = payload.role

    # Guardar cambios.
    await db.commit()

    # Actualizar el objeto desde la base de datos.
    await db.refresh(user)

    return user


# -----------------------------------------------------------------------------
# DELETE /api/users/{user_id}
# Elimina un usuario por su UUID.
# Si el usuario no existe se devuelve un error 404.
# -----------------------------------------------------------------------------
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> None:

    user = await db.get(User, user_id)

    if not user:
        raise NotFoundError("User not found")

    # Eliminar el usuario de la base de datos.
    await db.delete(user)

    # Confirmar los cambios.
    await db.commit()