from fastapi import APIRouter,Depends,status
from schemas.user import UserCreate
from models.user import User
from services.user_services import create_user
from db.session import get_database

router = APIRouter(prefix="/user", tags=["user"])

@router.post("", response_model=User,response_model_exclude={"hashed_password"}, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(user_data: UserCreate, db=Depends(get_database)) -> User:
    user = await create_user(user_data, db)  
    return user
 
  