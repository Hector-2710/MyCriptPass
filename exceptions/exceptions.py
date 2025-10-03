class UserAlreadyExistsError(Exception):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"User with email {email} already exists")

class NicknameAlreadyExistsError(Exception):
    def __init__(self, nickname: str):
        self.nickname = nickname
        super().__init__(f"User with nickname {nickname} already exists")
