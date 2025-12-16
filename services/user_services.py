from models.user import User
from motor.motor_asyncio import AsyncIOMotorDatabase 
from schemas.user import UserCreate, UserDelete, DeleteResponse
from core.security import get_password_hash, verify_password, create_access_token
from typing import Optional
from schemas.token import Token
from fastapi.security import OAuth2PasswordRequestForm
from exceptions.exceptions import UserAlreadyExistsError, NicknameAlreadyExistsError, UserNotFoundError,UnauthorizedError,IncorrectPasswordError

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

async def login_service(form_data: OAuth2PasswordRequestForm, db: AsyncIOMotorDatabase) -> Token:
    user = await get_user_by_nickname(form_data.username, db)
    if not user:
        raise UserNotFoundError(email=form_data.username)

    if not verify_password(form_data.password, user.hashed_password):
        raise IncorrectPasswordError(nickname=form_data.username)

    access_token = create_access_token({"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")

async def delete_user(email: str, db: AsyncIOMotorDatabase, current_user: User) -> DeleteResponse:
    existing_user = await get_user_by_email(email, db)
    if not existing_user:
        raise UserNotFoundError(email=email)

    if current_user.email != email and not getattr(current_user, "is_admin", False):
        raise UnauthorizedError(email=email)

    await db["users"].delete_one({"email": email})
    return DeleteResponse(success = True, detail=f"User {email} deleted successfully")
        
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