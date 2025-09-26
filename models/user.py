from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    full_name: str | None = Field(default=None)
    nickname: str | None = Field(default=None, index=True)
    role: str = Field(default="user")
    phone_number: str | None = Field(default=None)
    is_active: bool = Field(default=True)
    hashed_password: str