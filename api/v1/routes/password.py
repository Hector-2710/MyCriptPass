from annotated_types import Ge
from fastapi import APIRouter
from schemas.password import PasswordCreate, PasswordResponse
from services.password_services import create_password, get_password, delete_password
from db.session import get_database
from fastapi import Depends,status
from core.security import get_current_user
from exceptions.exceptions import PasswordNotFound
from schemas.password import GetPasswordResponse


router = APIRouter(prefix="/passwords", tags=["passwords"])

@router.post("/", summary="Crear una nueva contraseña",response_description="Contraseña creada exitosamente",response_model=PasswordResponse, status_code=status.HTTP_201_CREATED)
async def create_password_endpoint(password_data: PasswordCreate, User = Depends(get_current_user), db=Depends(get_database)) -> PasswordResponse:
    """
    Crea una nueva contraseña en la base de datos.
    - **nickname**: nickname del usuario
    - **service_name**: nombre del servicio
    - **password**: contraseña
    """
    password = await create_password(User.nickname, password_data, db)
    return password

@router.get("/{service_name}",summary="Obtener una contraseña",responses={404: {"model": PasswordNotFound, "description":"Contraseña no encontrada"}},response_model=GetPasswordResponse,response_description="Contraseña obtenida exitosamente", status_code=status.HTTP_200_OK)
async def get_password_endpoint(service_name: str, user = Depends(get_current_user), db=Depends(get_database)) -> GetPasswordResponse:
    """
    Obtiene una contraseña de la base de datos.
    - **nickname**: nickname del usuario
    - **service_name**: nombre del servicio
    """
    password = await get_password(user.nickname, service_name, db)
    return password

@router.delete("/{service_name}",summary="Eliminar una contraseña",responses={404: {"model": PasswordNotFound, "description":"Contraseña no encontrada"}},response_model=PasswordResponse,response_description="Contraseña eliminada exitosamente", status_code=status.HTTP_202_ACCEPTED)
async def delete_password_endpoint(service_name: str, user = Depends(get_current_user), db=Depends(get_database)) -> PasswordResponse:
    """
    Elimina una contraseña de la base de datos.
    - **nickname**: nickname del usuario
    - **service_name**: nombre del servicio
    """
    password = await delete_password(user.nickname, service_name, db)
    return password