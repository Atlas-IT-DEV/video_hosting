import time
from typing import Dict
import jwt

from config import Config


config = Config()

JWT_SECRET = config.__getattr__("JWT_SECRET")
JWT_ALGORITHM = config.__getattr__("JWT_ALGORITHM")

# возврат сгенерированных токенов
def token_response(token: str):
    return {
        "access_token": token
    }
    
# генерация токена с заданным сроком действия в секундах
def sign_jwt(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + config.__getattr__("TOKEN_TIME_WORK")
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