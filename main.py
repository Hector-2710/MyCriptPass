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

app = FastAPI(title="MyCryptPass API", version="1.0.0", lifespan=lifespan,description="API for managing user passwords securely")
app.include_router(user.router)
register_exception_handlers(app)

