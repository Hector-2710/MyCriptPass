import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from httpx import AsyncClient, ASGITransport
from main import app
from db.session import get_database as get_db
from core.config import settings

@pytest_asyncio.fixture
async def test_db_client():
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    yield client
    try:
        await client.drop_database(settings.DATABASE_TEST)
    finally:
        client.close()

@pytest_asyncio.fixture(autouse=True)
async def override_get_db(test_db_client):
    async def _get_test_db():
        return test_db_client["test_db"]
    
    app.dependency_overrides[get_db] = _get_test_db
    yield
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def ac():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client