from fastapi import APIRouter,Depends,status,Query
from schemas.user import UserCreate,UserDelete,DeleteResponse 
from models.user import User
from services.user_services import create_user,delete_user
from db.session import get_database

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", summary="Crear un nuevo usuario", response_model=User, response_model_exclude={"hashed_password"}, response_description="Usuario creado exitosamente", status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(user_data: UserCreate, db=Depends(get_database)) -> User:
    """
    Crea un nuevo usuario en la base de datos.
    - **email**: correo del usuario
    - **nickname**: alias único
    - **password**: contraseña (en hash)
    """
    user = await create_user(user_data, db)  
    return user

@router.delete("", summary="Eliminar un usuario", response_model=DeleteResponse, status_code=status.HTTP_202_ACCEPTED)
async def delete_user_endpoint(request: UserDelete, db=Depends(get_database)) -> DeleteResponse:
    """
    Elimina un usuario por su ID.
    """
    success = await delete_user(request, db)
    return success

  