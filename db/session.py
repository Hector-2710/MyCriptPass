from core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient

DATABASE_URL = settings.DATABASE_URL 
DATABASE_NAME = settings.DATABASE_NAME

client = AsyncIOMotorClient(DATABASE_URL)
db = client[DATABASE_NAME]

def get_database():
    return db