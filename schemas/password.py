from pydantic import BaseModel

class PasswordCreate(BaseModel):
    service_name: str
    password: str

class PasswordResponse(BaseModel):
    service_name: str

