from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
import jwt
from jwt import PyJWTError
from passlib.context import CryptContext

from src.core.repository import user_repository
from config import Config
from src.secure.secure_entity import Role, ROLE_HIERARCHY


config = Config()

SECRET_KEY = config.__getattr__("SECRET_KEY")
ALGORITHM = config.__getattr__("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(config.__getattr__("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(config.__getattr__("REFRESH_TOKEN_EXPIRE_DAYS"))

# hash password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# scheme authorize
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/token")


def create_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


# check user
def authenticate_user(phone: str, email: str):
    user = user_repository.get_user_by_email(email)

    if not user or user['phone'] != phone:
        return None
    
    return user


# decorator for secure routes by roles
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    return payload


# check role permissions
def role_required(min_role: str):
    def role_dependency(user: dict = Depends(get_current_user)):
        user_role = user.get("role")
        if ROLE_HIERARCHY.get(user_role, 0) < ROLE_HIERARCHY.get(min_role, 0):
            support_str = min_role.__str__()

            if support_str == 'A':
                support_str = 'admin'

            if support_str == 'M':
                support_str = 'course manager'

            if support_str == 'U':
                support_str = 'simple user'

            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not enough permissions. Need be {support_str}")
        return user
    return role_dependency
