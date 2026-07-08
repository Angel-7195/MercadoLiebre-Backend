from pydantic import BaseModel


# -----------------------------------------------------------------------------
# Esquemas de autenticación (Authentication Schemas)
#
# Estos esquemas definen el formato de las respuestas relacionadas con el
# inicio de sesión (login) y la autenticación mediante JWT.
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Esquema utilizado para devolver un token de acceso al cliente.
#
# Este esquema es enviado por el endpoint:
#     POST /api/auth/login
#
# Contiene la información necesaria para que el cliente pueda autenticarse
# en futuras peticiones a la API.
# -----------------------------------------------------------------------------
class TokenResponse(BaseModel):

    # Token JWT generado por el servidor.
    # El cliente debe enviarlo en el encabezado:
    # Authorization: Bearer <token>
    access_token: str

    # Tipo de token.
    # Normalmente siempre será "Bearer".
    token_type: str

    # Tiempo de expiración del token expresado en segundos.
    # Después de este tiempo el usuario deberá iniciar sesión nuevamente.
    expires_in_seconds: int