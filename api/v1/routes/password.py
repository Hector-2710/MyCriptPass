from fastapi import APIRouter
from schemas.password import PasswordCreate, PasswordResponse
from services.password_services import create_password, get_password
from db.session import get_database
from fastapi import Depends,status
from core.security import get_current_user


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

@router.get("/{service_name}", summary="Obtener una contraseña", response_description="Contraseña obtenida exitosamente", status_code=status.HTTP_200_OK)
async def get_password_endpoint(service_name: str, User = Depends(get_current_user), db=Depends(get_database)) :
    """
    Obtiene una contraseña de la base de datos.
    - **nickname**: nickname del usuario
    - **service_name**: nombre del servicio
    """
    password = await get_password(User.nickname, service_name, db)
    return password