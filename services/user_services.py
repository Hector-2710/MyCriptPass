from models.user import User
from motor.motor_asyncio import AsyncIOMotorDatabase 
from schemas.user import UserCreate, UserDelete, DeleteResponse
from core.security import get_password_hash
from typing import Optional, Any
from exceptions.exceptions import UserAlreadyExistsError, NicknameAlreadyExistsError, UserNotFoundError

async def create_user(user_data: UserCreate, db: AsyncIOMotorDatabase) -> User:
    existing_user = await get_user_by_email(user_data.email, db)
    existing_nickname = await get_user_by_nickname(user_data.nickname, db)

    if existing_user:
        raise UserAlreadyExistsError(email=user_data.email)
    if existing_nickname:
        raise NicknameAlreadyExistsError(nickname=user_data.nickname)

    hashed_password = get_password_hash(user_data.password)
    user_dict = user_data.model_dump(exclude={"password"})
    user_dict['hashed_password'] = hashed_password

    await db["users"].insert_one(user_dict)
    return User(**user_dict)

async def delete_user(user: UserDelete, db: AsyncIOMotorDatabase) ->  DeleteResponse:
    existing_user = await get_user_by_email(user.email, db)
    if not existing_user:
        raise UserNotFoundError(email=user.email)
    
    await db["users"].delete_one({"email": user.email})
    return DeleteResponse(success = True, detail=f"User {user.email} deleted successfully")
        

async def get_user_by_email(email: str, db: AsyncIOMotorDatabase) -> Optional[User]:
    user_data = await db["users"].find_one({"email": email})
    if user_data:
        return User(**user_data)
    return None

async def get_user_by_nickname(nickname: str, db: AsyncIOMotorDatabase) -> Optional[User]:
    user_data = await db["users"].find_one({"nickname": nickname})
    if user_data:
        return User(**user_data)
    return None