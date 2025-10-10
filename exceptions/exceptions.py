class AppBaseError(Exception):
    status_code: int = 400  

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class UserAlreadyExistsError(AppBaseError):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"User with email {email} already exists")

class NicknameAlreadyExistsError(AppBaseError):
    def __init__(self, nickname: str):
        self.nickname = nickname
        super().__init__(f"User with nickname {nickname} already exists")
