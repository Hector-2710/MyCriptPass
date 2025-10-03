from sqlmodel import SQLModel, Field
from pydantic import EmailStr

class User(SQLModel, table=True):
    id: int | None = Field(primary_key=True,unique= True)  
    email: EmailStr = Field(unique=True)
    full_name: str 
    nickname: str = Field(unique=True)
    phone_number: str 
    hashed_password: str