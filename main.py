from fastapi import FastAPI
from api.v1.routes import user,password
from exceptions.handlers import register_exception_handlers
from db.session import connect_to_mongo, close_mongo_connection
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

description = """
MyCryptPass es una API para almacenar y gestionar contraseñas de forma segura.
Proporciona gestión de usuarios (registro, autenticación) y un almacén de credenciales
(encriptadas) por usuario.

Características principales:
- Registro y autenticación de usuarios (contraseñas hasheadas).
- CRUD de entradas de contraseñas asociadas a cada usuario.
- Cifrado de secretos (cliente- o servidor-side según configuración).
- Índices y validaciones para evitar duplicados (email, nickname).
- Manejo centralizado de errores y respuesta consistente en JSON.
- Soporta operaciones asíncronas con Motor / MongoDB.

Seguridad:
- Almacena hashes para autenticación y datos cifrados para secretos.
"""

summary = "API para gestionar contraseñas de usuarios de forma segura"

app = FastAPI(title="MyCryptPass API",summary=summary,lifespan=lifespan, description=description, version="0.0.1")
app.include_router(user.router)
app.include_router(password.router)
register_exception_handlers(app)

