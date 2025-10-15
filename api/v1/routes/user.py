from fastapi import APIRouter,Depends,status,Query
from schemas.user import UserCreate,UserDelete,DeleteResponse 
from models.user import User
from services.user_services import create_user,delete_user,get_user_by_email,get_user_by_nickname
from db.session import get_database
from fastapi.security import OAuth2PasswordRequestForm
from core.security import verify_password,create_access_token,get_current_user
from fastapi import HTTPException

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
    
# ...existing code...
@router.post("/login",status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_database)):
    print("LOGIN attempt:", form_data.username)            # debug
    user = await get_user_by_nickname(form_data.username, db)
    print("Found user:", bool(user))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    ok = verify_password(form_data.password, user.hashed_password)
    print("Password match:", ok)
    if not ok:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.delete("/", summary="Eliminar un usuario", response_model=DeleteResponse, status_code=status.HTTP_202_ACCEPTED)
async def delete_user_endpoint(request: UserDelete, db=Depends(get_database), current_user: User = Depends(get_current_user)) -> DeleteResponse:
    """
    Elimina un usuario: solo el propio usuario o un admin pueden borrar.
    """
    # autorización básica: dueño o admin
    if current_user.email != request.email and not getattr(current_user, "is_admin", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para eliminar este usuario")

    result = await delete_user(request, db)
    return result