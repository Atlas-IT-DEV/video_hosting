from fastapi import APIRouter, HTTPException
from video_hosting.server.api.src.core.repository import config_color_repository
from src.core.models.models import ColorConfig
import typing

router = APIRouter(
    prefix="/api/color/config",
    tags=["Color configs CRUD"],
)


@router.get("/")
async def get_config_colors():
    page = config_color_repository.get_all_config_colors()
    return page


@router.get("/{id}")
async def get_config_color_by_id(id: int):
    config_color = config_color_repository.get_config_color_by_id(id)
    
    if not config_color:
        raise HTTPException(status_code=404, detail=f"ColorConfig with id {id} not found")
    
    return config_color


@router.post("/")
async def create_config_color(config_color: ColorConfig):
    config_color_id = config_color_repository.create_config_color(ColorConfig(**config_color.model_dump()))

    if not config_color_id:
        raise HTTPException(status_code=500, detail=f"All colors must be hex-color string")

    return {"message" : f"ColorConfig with id {config_color_id} create success"}


@router.put("/{id}")
async def update_config_color(id: int, config_color: ColorConfig):
    result = config_color_repository.update_config_color(id, config_color)

    if not result:
        raise HTTPException(status_code=404, detail=f"Color config with id {id} not found")

    return  {
        "message" : f"ColorConfig with id {id} update success",
        "new_config_color_data" : result
    }


@router.delete("/{id}")
async def delete_config_color(id: int):
    result = config_color_repository.delete_config_color_by_id(id)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Color config with id {id} not found")

    return {"message" : "ColorConfig delete success"}