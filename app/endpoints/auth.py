from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UnauthorizedError
from app.core.security import (
    create_access_token,
    get_access_token_expire_minutes,
    verify_password,
)
from app.database.session import get_db
from app.models.users import User
from app.schemas.auth import TokenResponse


# -----------------------------------------------------------------------------
# Router de autenticación.
#
# Este router contiene los endpoints relacionados con el inicio de sesión
# y la generación de tokens JWT.
# -----------------------------------------------------------------------------
router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
)


# -----------------------------------------------------------------------------
# POST /api/auth/login
#
# Permite a un usuario iniciar sesión utilizando su correo electrónico
# y contraseña.
#
# Si las credenciales son correctas:
#   - Se genera un token JWT.
#   - Se devuelve el token junto con su tiempo de expiración.
#
# Si las credenciales son incorrectas:
#   - Se devuelve un error HTTP 401 (Unauthorized).
# -----------------------------------------------------------------------------
@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:

    # -------------------------------------------------------------------------
    # Buscar el usuario utilizando el correo electrónico.
    #
    # OAuth2PasswordRequestForm utiliza el campo "username", por lo que
    # en este proyecto dicho campo corresponde al email del usuario.
    # -------------------------------------------------------------------------
    result = await db.execute(
        select(User).where(User.email == form_data.username)
    )

    user = result.scalar_one_or_none()

    # -------------------------------------------------------------------------
    # Verificar que:
    #   1. El usuario exista.
    #   2. La contraseña sea correcta.
    #
    # verify_password() compara la contraseña ingresada por el usuario
    # con el hash almacenado en la base de datos.
    # -------------------------------------------------------------------------
    if not user or not verify_password(
        form_data.password,
        user.password_hash,
    ):
        raise UnauthorizedError("Invalid credentials")

    # -------------------------------------------------------------------------
    # Generar el token JWT.
    #
    # Dentro del token se almacenan:
    #   - El UUID del usuario (subject).
    #   - El rol del usuario.
    # -------------------------------------------------------------------------
    access_token = create_access_token(
        subject=str(user.id),
        role=user.role,
    )

    # Tiempo de expiración expresado en segundos.
    expires_in_seconds = get_access_token_expire_minutes() * 60

    # -------------------------------------------------------------------------
    # Devolver el token al cliente.
    #
    # El cliente deberá enviarlo posteriormente en el encabezado:
    #
    # Authorization: Bearer <token>
    # -------------------------------------------------------------------------
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in_seconds=expires_in_seconds,
    )