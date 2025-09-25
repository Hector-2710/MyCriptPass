from fastapi import FastAPI
from api.v1.routes import user
from db.session import engine
from sqlmodel import SQLModel
from contextlib import asynccontextmanager
from models.user import User

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)  
    yield

app = FastAPI(title="MyCryptPass API", lifespan=lifespan)

app.include_router(user.app)