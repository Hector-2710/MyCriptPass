from core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient

DATABASE_URL = settings.DATABASE_URL 
DATABASE_NAME = settings.DATABASE_NAME

client = AsyncIOMotorClient(DATABASE_URL)
db = client[DATABASE_NAME]

def get_database():
    return db

async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    db = client[settings.DATABASE_NAME]

async def close_mongo_connection():
    global client
    if client:
        client.close()