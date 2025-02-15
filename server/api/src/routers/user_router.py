from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timedelta
from src.core.repository import user_repository
from src.core.models.models import User
from src.secure.main_secure import role_required, create_token, OAuth2PasswordRequestForm, authenticate_user, verify_token
from src.secure.secure_entity import Role
from config import Config


config = Config()

ACCESS_TOKEN_EXPIRE_MINUTES = int(config.__getattr__("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(config.__getattr__("REFRESH_TOKEN_EXPIRE_DAYS"))


router = APIRouter(
    prefix="/api/users",
    tags=["Users CRUD"],
)


# Эндпоинт получения токенов
@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    phone = form_data.username
    email = form_data.password

    user = authenticate_user(phone, email)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect phone or email")
    
    access_token = create_token({"sub": email, "role": user["role"]}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_token({"sub": email}, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh")
def refresh_token(refresh_token: str):
    payload = verify_token(refresh_token)
    user_email = payload.get("sub")

    if not user_email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    
    user = user_repository.get_user_by_email(user_email)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    new_access_token = create_token({"sub": user["email"], "role": user["role"]}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    return {"access_token": new_access_token, "token_type": "bearer"}


@router.get("/")
async def get_users(secure_data: dict = Depends(role_required(Role.ADMIN))):
    page = user_repository.get_all_users()
    return page


@router.get("/{id}")
async def get_user_by_id(id: int, secure_data: dict = Depends(role_required(Role.USER))):
    user = user_repository.get_user_by_id(id)
    
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    
    return user


@router.get("/{id}")
async def get_user_by_email(email: str, secure_data: dict = Depends(role_required(Role.USER))):
    user = user_repository.get_user_by_email(email)
    
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {email} not found")
    
    return user


@router.get("/{id}")
async def get_user_by_phone(phone: str, secure_data: dict = Depends(role_required(Role.USER))):
    user = user_repository.get_user_by_phone(phone)
    
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {phone} not found")
    
    return user


@router.post("/")
async def create_user(user: User):
    create_user = user_repository.create_user(User(**user.model_dump()))

    if not create_user:
        raise HTTPException(status_code=500, detail=f"User with this id, email or phone already exists")

    return {
        "message" : "User create success",
        "data" : create_user
    }


@router.put("/{id}")
async def update_user(id: int, user: User, secure_data: dict = Depends(role_required(Role.USER))):
    result = user_repository.update_user(id, user)

    if not result:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")

    return  {
        "message" : f"User with id {id} update success",
        "data" : result
    }


@router.delete("/{id}")
async def delete_user(id: int, secure_data: dict = Depends(role_required(Role.ADMIN))):
    result = user_repository.delete_user_by_id(id)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")

    return {"message" : "User delete success"}