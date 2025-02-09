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
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    
    return user


@router.post("/")
async def create_user(user: User):
    user_id = user_repository.create_user(User(**user.model_dump()))

    if not user_id:
        raise HTTPException(status_code=500, detail=f"User with this id, email or phone already exists")

    return {"message" : f"User with id {user_id} create success"}


@router.put("/{id}")
async def update_user(id: int, user: User):
    result = user_repository.update_user(id, user)

    if not result:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")

    return  {
        "message" : f"User with id {id} update success",
        "new_user_data" : result
    }


@router.delete("/{id}")
async def delete_user(id: int):
    result = user_repository.delete_user_by_id(id)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")

    return {"message" : "User delete success"}