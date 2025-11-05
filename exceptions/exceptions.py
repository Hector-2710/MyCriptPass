from fastapi import HTTPException

from pydantic import BaseModel

class ErrorResponse(BaseModel):
    detail: str


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
    def __init__(self, user: str):
        super().__init__(status_code=401, detail=f"You are not authorized to delete user {user}")

class IncorrectPasswordError(AppBaseError):
    def __init__(self, nickname: str):
        super().__init__(status_code=401, detail=f"Incorrect password for nickname {nickname}")

class PasswordAlreadyExistsError(AppBaseError):
    def __init__(self, nickname: str, service_name: str):
        super().__init__(status_code=409, detail=f"Password for service {service_name} already exists for nickname {nickname}")