import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import cloudinary_config
from app.core.handlers import register_error_handlers
from app.core.security import get_current_user
from app.endpoints.categories import router as categories_router
from app.endpoints.products import router as products_router
from app.endpoints.purchase_details import router as purchase_details_router
from app.endpoints.sellers import router as sellers_router
from app.endpoints.orders import router as orders_router
from app.endpoints.users import router as users_router
from app.endpoints.auth import router as auth_router

load_dotenv()


def _cors_origins() -> list[str]:
    raw = os.getenv(
        "CORS_ALLOW_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000",
    )
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


app = FastAPI(title="MercadoLiebre API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

register_error_handlers(app)

protected_dependencies = [Depends(get_current_user)]

app.include_router(users_router)
app.include_router(categories_router)
app.include_router(sellers_router)
app.include_router(products_router)
app.include_router(orders_router)
app.include_router(purchase_details_router)
app.include_router(auth_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}