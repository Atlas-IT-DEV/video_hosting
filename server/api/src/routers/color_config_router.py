from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from src.core.repository import config_color_repository
from src.core.models.models import ColorConfig
from typing import List, Optional, Annotated
from src.utils.file_operation import check_image_formant
from src.secure.main_secure import role_required
from src.secure.secure_entity import Role


router = APIRouter(
    prefix="/api/color/config",
    tags=["Color configs CRUD"],
)


@router.get("/")
async def get_config_colors(secure_data: dict = Depends(role_required(Role.MANAGER))):
    page = config_color_repository.get_all_config_colors()
    return page


@router.get("/{id}")
async def get_config_color_by_id(id: int, secure_data: dict = Depends(role_required(Role.MANAGER))):
    config_color = config_color_repository.get_config_color_by_id(id)
    
    if not config_color:
        raise HTTPException(status_code=404, detail=f"Color config with id {id} not found")
    
    return config_color


@router.post("/")
async def create_config_color(
    custom_color_1: Annotated[str, Form()] = None,
    custom_color_2: Annotated[str, Form()] = None,
    custom_color_3: Annotated[str, Form()] = None,
    custom_color_4: Annotated[str, Form()] = None, 
    custom_color_5: Annotated[str, Form()] = None,
    files: Optional[List[UploadFile]] = File(None),
    secure_data: dict = Depends(role_required(Role.MANAGER))
):
    if files:
        result = check_image_formant(files)

        if not result:
            raise HTTPException(status_code=500, detail={
                    "status": "error",
                    "msg": f"All image must be in png/jpg/jpeg format"
                })

    color_config = ColorConfig(
        id=0,
        custom_color_1=custom_color_1, 
        custom_color_2=custom_color_2,
        custom_color_3=custom_color_3, 
        custom_color_4=custom_color_4, 
        custom_color_5=custom_color_5
    )
    
    create_color_config = config_color_repository.create_config_color(color_config, files)

    if not create_color_config:
        raise HTTPException(status_code=500, detail=f"All colors must be hex-color string")

    return {
        "message" : "Color config create success",
        "data" : create_color_config
    }


@router.put("/{id}")
async def update_config_color(
    id: int,
    custom_color_1: Annotated[str, Form()] = None,
    custom_color_2: Annotated[str, Form()] = None,
    custom_color_3: Annotated[str, Form()] = None,
    custom_color_4: Annotated[str, Form()] = None, 
    custom_color_5: Annotated[str, Form()] = None,
    files: Optional[List[UploadFile]] = File(None),
    secure_data: dict = Depends(role_required(Role.MANAGER))                              
):
    if files:
        result = check_image_formant(files)

        if not result:
            raise HTTPException(status_code=500, detail={
                    "status": "error",
                    "msg": f"All image must be in png/jpg/jpeg format"
                })
        
    color_config = ColorConfig(
        id=id,
        custom_color_1=custom_color_1, 
        custom_color_2=custom_color_2,
        custom_color_3=custom_color_3, 
        custom_color_4=custom_color_4, 
        custom_color_5=custom_color_5
    )
        
    result = config_color_repository.update_config_color(id, color_config, files)

    if not result:
        raise HTTPException(status_code=404, detail=f"Color config with id {id} not found")

    return  {
        "message" : f"Color config with id {id} update success",
        "data" : result
    }


@router.delete("/{id}")
async def delete_config_color(id: int, secure_data: dict = Depends(role_required(Role.MANAGER))):
    result = config_color_repository.delete_config_color_by_id(id)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Color config with id {id} not found")

    return {"message" : "Color config delete success"}