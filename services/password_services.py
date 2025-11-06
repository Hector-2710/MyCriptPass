from motor.motor_asyncio import AsyncIOMotorDatabase
from schemas.password import PasswordCreate, PasswordResponse
from exceptions.exceptions import PasswordAlreadyExistsError, PasswordNotFoundError
from core.security import get_password_hash

async def create_password(nickname: str, password_data: PasswordCreate, db: AsyncIOMotorDatabase) -> PasswordResponse:
    existing = await exists_password_for_service(nickname, password_data.service_name, db)
    if existing:
        raise PasswordAlreadyExistsError(nickname=nickname, service_name=password_data.service_name)

    hashed_password = get_password_hash(password_data.password)

    await db["users"].update_one(
        {"nickname": nickname},
        {"$push": {"passwords": {"app_service": password_data.service_name, "password": hashed_password}}}
    )

    return {"service_name": password_data.service_name}


async def get_password(nickname: str, service_name: str, db: AsyncIOMotorDatabase) -> PasswordResponse:
    exists = await exists_password_for_service(nickname, service_name, db)
    if not exists:
        return PasswordNotFoundError(nickname=nickname, service_name=service_name)
    password = await db["users"].find_one(
        {"nickname": nickname, "passwords.app_service": service_name},
        {"passwords.$": 1, "_id": 0},
    )
    print(password)
    return password
    
async def exists_password_for_service(nickname: str, service_name: str, db: AsyncIOMotorDatabase) -> bool:
    doc = await db["users"].find_one(
        {"nickname": nickname, "passwords.app_service": service_name},
        {"_id": 1},
    )
    if doc:
        return True
    return False
