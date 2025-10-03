from pydantic import BaseModel, EmailStr,Field
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr =  Field(...,description="The email of the user")
    full_name: str = Field(..., description="The full name of the user", min_length=10, max_length=70)
    nickname: str = Field(..., description="The nickname of the user", min_length=3, max_length=13)
    phone_number: Optional[str] = Field(default=None, description="The phone number of the user", min_length=8, max_length=15)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    