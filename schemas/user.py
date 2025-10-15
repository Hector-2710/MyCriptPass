from pydantic import BaseModel, EmailStr,Field

class UserBase(BaseModel):
    full_name: str = Field(..., description="The full name of the user", min_length=10, max_length=70)
    email: EmailStr =  Field(...,description="The email of the user")
    nickname: str = Field(..., description="The nickname of the user", min_length=3, max_length=13)

    model_config = {"extra": "forbid"}  

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")

class UserDelete(BaseModel):
    email: EmailStr = Field(..., description="The email of the user to delete")

class DeleteResponse(BaseModel):
    success: bool = Field(..., description="Indicates if the deletion was successful")
    detail: str = Field(..., description="Details about the deletion process")

