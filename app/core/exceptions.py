"""
Excepciones personalizadas para MercadoLiebre.

Todas las excepciones de la aplicación heredan de AppError
para permitir un manejo centralizado de errores mediante
los exception handlers de FastAPI.
"""


class AppError(Exception):
    """Clase base para todas las excepciones de la aplicación."""

    def __init__(self, message: str, code: str, status_code: int):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)


class NotFoundError(AppError):
    """Se lanza cuando un recurso no existe."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(
            message=message,
            code="RESOURCE_NOT_FOUND",
            status_code=404,
        )


class ConflictError(AppError):
    """Se lanza cuando existe un conflicto con los datos."""

    def __init__(self, message: str = "Data conflict"):
        super().__init__(
            message=message,
            code="DATA_CONFLICT",
            status_code=409,
        )


class ValidationError(AppError):
    """Se lanza cuando los datos enviados no son válidos."""

    def __init__(self, message: str = "Validation error"):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=400,
        )


class UnauthorizedError(AppError):
    """Se lanza cuando el usuario no está autenticado."""

    def __init__(self, message: str = "Unauthorized"):
        super().__init__(
            message=message,
            code="UNAUTHORIZED",
            status_code=401,
        )


class ForbiddenError(AppError):
    """Se lanza cuando el usuario no tiene permisos suficientes."""

    def __init__(self, message: str = "Forbidden"):
        super().__init__(
            message=message,
            code="FORBIDDEN",
            status_code=403,
        )