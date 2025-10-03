from sqlmodel import Session, select
from models.user import User
from schemas.user import UserCreate
from core.security import get_password_hash
from typing import Optional
from exceptions.exceptions import UserAlreadyExistsError, NicknameAlreadyExistsError

def create_user(session: Session, user_data: UserCreate) -> User:
    existing_user = get_user_by_email(session, user_data.email)
    existing_nickname = get_user_by_nickname(session, user_data.nickname)

    if existing_user:
        raise UserAlreadyExistsError(email=user_data.email)
    
    if existing_nickname:
        raise NicknameAlreadyExistsError(nickname=user_data.nickname)

    hashed_password = get_password_hash(user_data.password)
    user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        nickname=user_data.nickname,
        phone_number=user_data.phone_number,
        hashed_password=hashed_password
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user_by_email(session: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()

def get_user_by_nickname(session: Session, nickname: str) -> Optional[User]:
    statement = select(User).where(User.nickname == nickname)
    return session.exec(statement).first()