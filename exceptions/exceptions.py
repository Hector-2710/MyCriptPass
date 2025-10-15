from fastapi import HTTPException

class AppBaseError(HTTPException):
    def __init__(self, status_code: int, message: str):
        super().__init__(status_code=status_code, detail=message)
        
class UserAlreadyExistsError(AppBaseError):
    def __init__(self, email: str):
        super().__init__(status_code=409, message=f"User with email {email} already exists")

class NicknameAlreadyExistsError(AppBaseError):
    def __init__(self, nickname: str):
        super().__init__(status_code=409, message=f"User with nickname {nickname} already exists")

class UserNotFoundError(AppBaseError):
    def __init__(self, email: str):
        super().__init__(status_code=404, message=f"User with email {email} not found")
