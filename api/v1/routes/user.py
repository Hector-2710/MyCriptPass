from fastapi import APIRouter,Depends,status
from schemas.user import UserCreate,DeleteResponse
from models.user import User
from services.user_services import create_user,delete_user,login_service
from db.session import get_database
from schemas.token import Token
from fastapi.security import OAuth2PasswordRequestForm
from core.security import get_current_user
from exceptions.exceptions import UserExists,Unauthorized

router = APIRouter(prefix="/users",tags=["users"])

@router.post("/", summary="Crear un nuevo usuario",response_model=User,responses={409: {"model": UserExists, "description":"Conflicto: el usuario ya existe"}}, response_model_exclude={"hashed_password"}, response_description="Usuario creado exitosamente", status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(user_data: UserCreate, db=Depends(get_database)) -> User:
    """
    Crea un nuevo usuario en la base de datos
    - **email**: correo del usuario
    - **nickname**: alias único
    - **password**: contraseña (en hash)
    - **full_name**: nombre completo del usuario
    """
    user = await create_user(user_data, db) 
    return user 
    
@router.post("/login",responses={401: {"model": Unauthorized, "description":" El usuario no está autorizado para acceder"}},summary="Iniciar sesión", response_model=Token,response_description="Inicia sesión y devuelve un token de acceso",status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_database)):
    """
    Endpoint para el login de usuarios.
    - **username**: nickname del usuario
    - **password**: contraseña del usuario
    """
    return await login_service(form_data, db)

@router.delete("/{user_email}", summary="Eliminar un usuario", response_model=DeleteResponse, status_code=status.HTTP_202_ACCEPTED)
async def delete_user_endpoint(user_email: str, db=Depends(get_database), current_user: User = Depends(get_current_user)) -> DeleteResponse:
    """
    Elimina un usuario: solo el propio usuario o un admin pueden borrar.
    """
    return await delete_user(user_email, db, current_user)