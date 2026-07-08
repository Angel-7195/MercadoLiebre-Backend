import asyncio
import uuid

from sqlalchemy import select

from app.database.session import AsyncSessionLocal
from app.core.security import hash_password
from app.models.users import User

async def seed_users():
    """Crear usuarios iniciales si no existen"""
    async with AsyncSessionLocal() as db:
        try:
            users_data = [
                {
                    "email": "admin@admin.com",
                    "password": "Admin123!",
                    "full_name": "Administrador",
                    "role": "ADMIN"
                },
                {
                    "email": "angel@correo.com",
                    "password": "Angel123!",
                    "full_name": "Angel Gutiérrez",
                    "role": "CLIENT",
                },
            ]

            for user_data in users_data:
                result = await db.execute(
                    select(User).where(User.email == user_data["email"])
                )
                user = result.scalar_one_or_none()

                if not user:
                    new_user = User(
                        id=str(uuid.uuid4()),
                        email=user_data["email"],
                        password_hash=hash_password(user_data["password"]),
                        full_name=user_data["full_name"],
                        role=user_data["role"],
                    )
                    db.add(new_user)
                    await db.commit()
                    print(f"Usuario {user_data['email']} creado exitosamente.")
                else:
                    print(f"Usuario {user_data['email']} ya existe.")

            await db.commit()

        except Exception as e:
            await db.rollback()
            print(f"Error al crear usuarios: {e}")
            raise

async def main():
    await seed_users()

if __name__ == "__main__":
    asyncio.run(main())