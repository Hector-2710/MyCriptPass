from fastapi import APIRouter
from schemas.user import UserCreate
from models.user import User
from services.user_services import create_user
from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from db.session import get_session
from exceptions.exceptions import UserAlreadyExistsError, NicknameAlreadyExistsError

app = APIRouter(prefix="/user", tags=["user"])

@app.post("/create", response_model=User,response_model_exclude={"hashed_password"}, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user_data: UserCreate, session: Session = Depends(get_session)) -> User:
    try:
        user = create_user(session, user_data)  
        return user
    
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except NicknameAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
