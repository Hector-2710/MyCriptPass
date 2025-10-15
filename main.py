from fastapi import FastAPI
from api.v1.routes import user
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
(encriptadas) por usuario. Está pensada para integrarse con clientes web y móviles.

Características principales:
- Registro y autenticación de usuarios (contraseñas hasheadas).
- CRUD de entradas de contraseñas asociadas a cada usuario.
- Cifrado de secretos (cliente- o servidor-side según configuración).
- Índices y validaciones para evitar duplicados (email, nickname).
- Manejo centralizado de errores y respuesta consistente en JSON.
- Soporta operaciones asíncronas con Motor / MongoDB.

Seguridad:
- Nunca se devuelven contraseñas en claro ni campos sensibles en las respuestas.
- Almacena hashes para autenticación y datos cifrados para secretos.
- Revise y configure la gestión de claves y políticas de rotación en producción.

Documentación:
- Endpoints disponibles en la ruta /docs (OpenAPI/Swagger).
- Revisar schemas en schemas/ para ver validaciones y campos expuestos.
"""

summary = "API para gestionar contraseñas de usuarios de forma segura"

app = FastAPI(title="MyCryptPass API",summary=summary,lifespan=lifespan, description=description, version="0.0.1")
app.include_router(user.router)
register_exception_handlers(app)

