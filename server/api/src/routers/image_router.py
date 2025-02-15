from typing import Annotated, List, Optional
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, Depends
from src.core.repository import images_repository
from src.core.models.models import Image, ImageLevelEnum
from src.utils.file_operation import check_image_formant
from src.secure.main_secure import role_required
from src.secure.secure_entity import Role

router = APIRouter(
    prefix="/api/images",
    tags=["Images CRUD"],
)


@router.post("/")
async def create_single_image(
    type: Annotated[str, Form()] = None,
    level: Annotated[str, Form()] = None,
    position: Annotated[int, Form()] = None,
    object_id: Annotated[int, Form()] = None,
    file: Optional[UploadFile] = File(None),
    secure_data: dict = Depends(role_required(Role.MANAGER)),
):
    if file:
        result = check_image_formant([file])

        if not result:
            raise HTTPException(status_code=500, detail={
                    "status": "error",
                    "msg": f"Image must be in png/jpg/jpeg format"
                })
        
    if level != ImageLevelEnum.MAIN and level != ImageLevelEnum.ADDITIONAL:
        raise HTTPException(status_code=404, detail=f"Incorrect level value")
    
    if position < 0:
        raise HTTPException(status_code=404, detail=f"Incorrect position value")
        
    image = Image(id=0, type=type, level=level, position=position, object_id=object_id, path="CHANGE_ME")

    create_image = images_repository.create_single_image(image, file)

    if not create_image:
        raise HTTPException(status_code=500, detail=f"Error of create image")

    return {
        "message" : "Image create success",
        "data" : create_image
    }


@router.put("/{id}")
async def update_single_image(id: int, level: str, position: int, secure_data: dict = Depends(role_required(Role.MANAGER))):
    if level != ImageLevelEnum.MAIN and level != ImageLevelEnum.ADDITIONAL:
        raise HTTPException(status_code=404, detail=f"Incorrect level value")
    
    if position < 0:
        raise HTTPException(status_code=404, detail=f"Incorrect position value")
    
    result = images_repository.update_image_level_and_position(id, level, position)

    if not result:
        raise HTTPException(status_code=404, detail=f"Image with id {id} not found")

    return  {
        "message" : f"Image with id {id} update success",
        "data" : result
    }


@router.delete("/{id}")
async def delete_single_image(id: int, secure_data: dict = Depends(role_required(Role.MANAGER))):
    result = images_repository.delete_single_image_by_id(id)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Image with id {id} not found")

    return {"message" : "Image delete success"}