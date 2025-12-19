from fastapi import HTTPException

from pydantic import BaseModel

class EmailExists(BaseModel):
    detail: str = "User already exists"

class NicknameExists(BaseModel):
    detail: str = "Nickname already exists"

class Unauthorized(BaseModel):
    detail: str = "You are not authorized to delete user"

class PasswordNotFound(BaseModel):
    detail: str = "Password not found"

class PasswordAlreadyExists(BaseModel):
    detail: str = "Password already exists"

class UserNotFound(BaseModel):
    detail: str = "User not found"

class IncorrectPassword(BaseModel):
    detail: str = "Incorrect password"

class AppBaseError(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)
        
class UserAlreadyExistsError(AppBaseError):
    def __init__(self, email: str):
        super().__init__(status_code=409, detail=f"User with email {email} already exists")

class NicknameAlreadyExistsError(AppBaseError):
    def __init__(self, nickname: str):
        super().__init__(status_code=499, detail=f"User with nickname {nickname} already exists")

class UserNotFoundError(AppBaseError):
    def __init__(self, email: str):
        super().__init__(status_code=404, detail=f"User with email {email} not found")

class UnauthorizedError(AppBaseError):
    def __init__(self, email: str):
        super().__init__(status_code=401, detail=f"You are not authorized to delete email {email}")

class IncorrectPasswordError(AppBaseError):
    def __init__(self, nickname: str):
        super().__init__(status_code=401, detail=f"Incorrect password for nickname {nickname}")

class PasswordAlreadyExistsError(AppBaseError):
    def __init__(self, nickname: str, service_name: str):
        super().__init__(status_code=409, detail=f"Password for service {service_name} already exists for nickname {nickname}")

class PasswordNotFoundError(AppBaseError):
    def __init__(self, nickname: str, service_name: str):
        super().__init__(status_code=404, detail=f"Password for service {service_name} not found for nickname {nickname}")