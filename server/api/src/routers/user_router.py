from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from src.core.repository import user_repository
from src.core.models.models import User
from src.secure.main_secure import role_required, create_token, OAuth2PasswordRequestForm, authenticate_user, verify_token
from src.secure.secure_entity import Role
from config import Config
import json
import urllib.request
import httpx


config = Config()

ACCESS_TOKEN_EXPIRE_MINUTES = int(config.__getattr__("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(config.__getattr__("REFRESH_TOKEN_EXPIRE_DAYS"))


router = APIRouter(
    prefix="/api/users",
    tags=["Users CRUD"],
)


# get token
@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    email = form_data.username
    phone = form_data.password

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

@router.post("/auth/google")
async def google_auth(code: str):
    """Обмениваем Authorization Code на Access Token + Refresh Token"""
    token_url = "https://oauth2.googleapis.com/token"

    data = {
        "client_id": "139259050435-62e07h09fod6e3e37mfl7vin0ds9h5o4.apps.googleusercontent.com",
        "client_secret": "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",
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": "http://localhost:3000",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    tokens = response.json()
    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens.get("refresh_token"),  # Может отсутствовать, если нет `access_type=offline`
        "expires_in": tokens["expires_in"],
        "token_type": tokens["token_type"],
    }

TOKEN_URL = "https://oauth2.googleapis.com/token"

@router.post("/auth/google/refresh")
async def refresh_token(refresh_token: str):
    """Обновляет access_token с помощью refresh_token"""

    data = {
        "client_id": "139259050435-62e07h09fod6e3e37mfl7vin0ds9h5o4.apps.googleusercontent.com",
        "client_secret": "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",
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(TOKEN_URL, data=data)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    tokens = response.json()
    return {
        "access_token": tokens["access_token"],
        "expires_in": tokens["expires_in"],
        "token_type": tokens["token_type"],
    }


@router.get("/")
async def get_users(secure_data: dict = Depends(role_required(Role.ADMIN))):
    page = user_repository.get_all_users()
    return page


@router.get("/{id}")
async def get_user_by_id(id: str, secure_data: dict = Depends(role_required(Role.USER))):
    user = user_repository.get_user_by_id(id)
    
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    
    return user


@router.get("/{email}")
async def get_user_by_email(email: str, secure_data: dict = Depends(role_required(Role.USER))):
    user = user_repository.get_user_by_email(email)
    
    if not user:
        raise HTTPException(status_code=404, detail=f"User with email {email} not found")
    
    return user


@router.get("/{phone}")
async def get_user_by_phone(phone: str, secure_data: dict = Depends(role_required(Role.USER))):
    user = user_repository.get_user_by_phone(phone)
    
    if not user:
        raise HTTPException(status_code=404, detail=f"User with phone {phone} not found")
    
    return user


@router.post("/")
async def create_user(user: User):
    create_user = user_repository.create_user(User(**user.model_dump()))

    if not create_user:
        raise HTTPException(status_code=500, detail=f"User with this id, email or phone already exists")
    
    access_token = create_token({"sub": user.email, "role": user.role}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_token({"sub": user.email}, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

    return {
        "message" : "User create success",
        "data" : create_user,
        "access_token": access_token, 
        "refresh_token": refresh_token, 
        "token_type": "bearer"
    }


@router.put("/{id}")
async def update_user(id: str, user: User, secure_data: dict = Depends(role_required(Role.USER))):
    result = user_repository.update_user(id, user)

    if not result:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")

    return  {
        "message" : f"User with id {id} update success",
        "data" : result
    }


@router.delete("/{id}")
async def delete_user(id: str, secure_data: dict = Depends(role_required(Role.ADMIN))):
    result = user_repository.delete_user_by_id(id)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")

    return {"message" : "User delete success"}