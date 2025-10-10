from models.user import User
from schemas.user import UserCreate
from core.security import get_password_hash
from typing import Optional, Any
from exceptions.exceptions import UserAlreadyExistsError, NicknameAlreadyExistsError

async def create_user(user_data: UserCreate, db=Any) -> User:
    existing_user = await get_user_by_email(user_data.email, db)
    existing_nickname = await get_user_by_nickname(user_data.nickname, db)

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

async def get_user_by_email(email: str, db=Any) -> Optional[User]:
    user_data = await db["users"].find_one({"email": email})
    if user_data:
        return User(**user_data)
    return None

async def get_user_by_nickname(nickname: str, db=Any) -> Optional[User]:
    user_data = await db["users"].find_one({"nickname": nickname})
    if user_data:
        return User(**user_data)
    return None