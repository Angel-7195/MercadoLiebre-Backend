# 🛒 MercadoLiebre Backend

Backend desarrollado con **FastAPI** inspirado en una plataforma de comercio electrónico similar a Mercado Libre.

El proyecto implementa una arquitectura cliente-servidor utilizando PostgreSQL como base de datos, SQLAlchemy como ORM y Alembic para el control de migraciones. Además incluye autenticación mediante JWT y un cliente CRUD desde consola para administrar todas las entidades del sistema.

---

# Características

- Autenticación mediante JWT.
- CRUD completo para todas las entidades.
- Arquitectura REST.
- Base de datos PostgreSQL.
- SQLAlchemy 2.0 (ORM).
- Migraciones con Alembic.
- Validación mediante Pydantic.
- Cliente CRUD desde consola.
- Manejo centralizado de errores.
- Variables de entorno mediante python-dotenv.

---

# Tecnologías utilizadas

- Python 3.12+
- FastAPI
- SQLAlchemy 2.0
- PostgreSQL
- Neon Database
- Alembic
- Pydantic
- JWT
- HTTPX
- Rich
- Uvicorn

---

# Estructura del proyecto

```
mercadoliebre-backend/
│
├── .github/
│   └── workflows/                     # Pipeline de Integración Continua (CI/CD)
│
├── alembic/                           # Configuración de migraciones de la base de datos
│   ├── versions/                      # Historial de migraciones
│   └── env.py                         # Configuración del entorno de Alembic
│
├── app/
│   ├── core/                          # Configuración y lógica central de la aplicación
│   │   ├── exceptions.py              # Excepciones personalizadas
│   │   ├── handlers.py                # Manejadores globales de errores
│   │   └── security.py                # Autenticación JWT, hashing y seguridad
│   │
│   ├── crud/                          # Cliente HTTP para consumir la API desde consola
│   │   ├── auth.py                    # Operaciones de autenticación
│   │   ├── users.py                   # CRUD de usuarios
│   │   ├── sellers.py                 # CRUD de vendedores
│   │   ├── categories.py              # CRUD de categorías
│   │   ├── products.py                # CRUD de productos
│   │   ├── orders.py                  # CRUD de órdenes
│   │   ├── purchase_details.py        # CRUD de detalles de compra
│   │   ├── menu_users.py              # Menú CRUD de usuarios
│   │   ├── menu_sellers.py            # Menú CRUD de vendedores
│   │   ├── menu_categories.py         # Menú CRUD de categorías
│   │   ├── menu_products.py           # Menú CRUD de productos
│   │   ├── menu_orders.py             # Menú CRUD de órdenes
│   │   ├── menu_purchase_details.py   # Menú CRUD de detalles de compra
│   │   └── http_client.py             # Cliente HTTP reutilizable para consumir la API
│   │
│   ├── database/                      # Configuración de la base de datos
│   │   ├── base.py                    # Clase Base de SQLAlchemy
│   │   ├── session.py                 # Gestión de sesiones asíncronas
│   │   └── seeder.py                  # Inserción de datos iniciales
│   │
│   ├── endpoints/                     # Endpoints (routers) de FastAPI
│   │   ├── auth.py                    # Endpoints de autenticación
│   │   ├── users.py                   # Endpoints de usuarios
│   │   ├── sellers.py                 # Endpoints de vendedores
│   │   ├── categories.py              # Endpoints de categorías
│   │   ├── products.py                # Endpoints de productos
│   │   ├── orders.py                  # Endpoints de órdenes
│   │   └── purchase_details.py        # Endpoints de detalles de compra
│   │
│   ├── models/                        # Modelos ORM (tablas de PostgreSQL)
│   │   ├── __init__.py                # Inicialización del paquete models
│   │   ├── users.py                   # Modelo de usuarios
│   │   ├── sellers.py                 # Modelo de vendedores
│   │   ├── categories.py              # Modelo de categorías
│   │   ├── products.py                # Modelo de productos
│   │   ├── orders.py                  # Modelo de órdenes
│   │   └── purchase_details.py        # Modelo de detalles de compra
│   │
│   ├── schemas/                       # Modelos Pydantic para validación y serialización
│   │   ├── __init__.py                # Inicialización del paquete schemas
│   │   ├── auth.py                    # Esquemas de autenticación
│   │   ├── users.py                   # Esquemas de usuarios
│   │   ├── sellers.py                 # Esquemas de vendedores
│   │   ├── categories.py              # Esquemas de categorías
│   │   ├── products.py                # Esquemas de productos
│   │   ├── orders.py                  # Esquemas de órdenes
│   │   └── purchase_details.py        # Esquemas de detalles de compra
│   │
│   ├── utils/                         # Funciones auxiliares reutilizables
│   │   ├── cli_utils.py               # Utilidades para la interfaz de consola
│   │   └── menu_utils.py              # Componentes reutilizables para los menús CRUD
│   │
│   ├── app.py                         # Configuración principal de FastAPI
│   └── main.py                        # Punto de entrada del cliente CRUD por consola
│
├── tests/                             # Pruebas unitarias e integración
│
├── .env.example                       # Ejemplo de variables de entorno
├── .gitignore                         # Archivos ignorados por Git
├── alembic.ini                        # Configuración general de Alembic
├── requirements.txt                   # Dependencias del proyecto
└── README.md                          # Documentación del proyecto
```

---

# Entidades

El sistema administra las siguientes entidades:

- Users
- Sellers
- Categories
- Products
- Orders
- Purchase Details

---

# Instalación

Clonar el repositorio

```bash
git clone https://github.com/TU-USUARIO/MercadoLiebre-Backend.git

cd MercadoLiebre-Backend
```

Crear un entorno virtual

Windows

```bash
python -m venv .venv
```

Linux

```bash
python3 -m venv .venv
```

Activar el entorno

Windows

```bash
.venv\Scripts\activate
```

Linux

```bash
source .venv/bin/activate
```

Instalar dependencias

```bash
python -m pip install -r requirements.txt
```

---

# Variables de entorno

Crear un archivo `.env`

```env
DATABASE_URL=postgresql+asyncpg://usuario:password@host/database

SECRET_KEY=tu_clave

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60

API_BASE_URL=http://127.0.0.1:8000
```

---

# Migraciones

Crear una migración

```bash
alembic revision --autogenerate -m "mensaje"
```

Aplicar migraciones

```bash
alembic upgrade head
```

---

# Ejecutar el servidor

```bash
fastapi dev app/main.py
```

o

```bash
python -m uvicorn app.main:app --reload
```

---

# Poblar la base de datos

```bash
python -m app.database.seeder
```

---

# Ejecutar el cliente CRUD

```bash
python -m main.py
```

Desde la consola podrás administrar:

- Usuarios
- Vendedores
- Categorías
- Productos
- Órdenes
- Detalles de compra

---

# Dependencias

Las principales dependencias utilizadas son:

- fastapi
- uvicorn
- sqlalchemy
- asyncpg
- alembic
- python-dotenv
- pydantic
- email-validator
- python-multipart
- PyJWT
- bcrypt
- httpx
- rich
- pytest
- black
- ruff

---

# API

La documentación interactiva se encuentra en:

```
http://127.0.0.1:8000/docs
```

Documentación ReDoc:

```
http://127.0.0.1:8000/redoc
```

---

# Autor

Ángel David Gutiérrez Ladino

Tecnología en Desarrollo de Software

Instituto Tecnológico Metropolitano (ITM)