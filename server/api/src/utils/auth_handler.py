# app/auth/auth_handler.py

import time
from typing import Dict

import jwt


JWT_SECRET = "please_please_update_me_please"
JWT_ALGORITHM = "HS256"

# возврат сгенерированных токенов
def token_response(token: str):
    return {
        "access_token": token
    }
    
# генерация токена со сроком действия 60 минут
def sign_jwt(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 3600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)

# проверка токена на время действия - вернёт None, если вышло
def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}