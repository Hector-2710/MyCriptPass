from models.user import User
from schemas.user import UserCreate
from core.security import get_password_hash
from db.session import get_database
from typing import Optional
from exceptions.exceptions import UserAlreadyExistsError, NicknameAlreadyExistsError

db = get_database()

async def create_user(user_data: UserCreate) -> User:
    existing_user = await get_user_by_email(user_data.email)
    existing_nickname = await get_user_by_nickname(user_data.nickname)

    if existing_user:
        raise UserAlreadyExistsError(email=user_data.email)
    if existing_nickname:
        raise NicknameAlreadyExistsError(nickname=user_data.nickname)

    hashed_password = get_password_hash(user_data.password)
    user_dict = user_data.model_dump()
    user_dict['hashed_password'] = hashed_password
    user_dict.pop('password', None)  

    await db["users"].insert_one(user_dict)
    return User(**user_dict)

async def get_user_by_email(email: str) -> Optional[User]:
    user_data = await db["users"].find_one({"email": email})
    if user_data:
        return User(**user_data)
    return None

async def get_user_by_nickname(nickname: str) -> Optional[User]:
    user_data = await db["users"].find_one({"nickname": nickname})
    if user_data:
        return User(**user_data)
    return None