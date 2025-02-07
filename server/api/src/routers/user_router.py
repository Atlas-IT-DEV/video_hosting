from fastapi import APIRouter, HTTPException
from src.core.repository import user_repository
from src.core.models.models import User
import typing

router = APIRouter(
    prefix="/api/users",
    tags=["Users CRUD"],
)

@router.get("/")
async def get_users():
    page = user_repository.get_all_users()
    return page

@router.get("/{id}")
async def get_user_by_id(id: int):
    user = user_repository.get_user_by_id(id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.post("/")
async def create_user(user: User):
    user_id = user_repository.create_user(User(**user.model_dump()))
    return user_id

# @router.put("/{id}")
# async def update_sport(id: int, sport: SportOut):
#     sport = user_repository.updateSport(id, sport)
#     return sport

# @router.delete("/{id}")
# async def delete_sport(id: int):
#     result = user_repository.deleteSportById(id)
    
#     if not result:
#         raise HTTPException(status_code=404, detail="Sport not found")

#     return {"message" : "Sport delete success"}