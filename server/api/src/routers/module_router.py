from typing import Annotated, List, Optional
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from src.core.repository import module_repository
from src.core.models.models import Module
from src.utils.file_operation import check_image_formant


router = APIRouter(
    prefix="/api/modules",
    tags=["Modules CRUD"],
)


@router.get("/")
async def get_modules():
    page = module_repository.get_all_modules()
    return page


@router.get("/{id}")
async def get_module_by_id(id: int):
    module = module_repository.get_module_by_id(id)
    
    if not module:
        raise HTTPException(status_code=404, detail=f"Module with id {id} not found")
    
    return module


@router.post("/")
async def create_module(
    course_id: Annotated[int, Form()] = None,
    title: Annotated[str, Form()] = None,
    description: Annotated[str, Form()] = None,
    position: Annotated[int, Form()] = None,
    created_at: Annotated[int, Form()] = None, 
    files: Optional[List[UploadFile]] = File(None)
):
    if files:
        result = check_image_formant(files)

        if not result:
            raise HTTPException(status_code=500, detail={
                    "status": "error",
                    "msg": f"All image must be in png/jpg/jpeg format"
                })
        
    module = Module(id=0, course_id=course_id, title=title, description=description, position=position, created_at=created_at)

    create_module = module_repository.create_module(module, files)

    if not create_module:
        raise HTTPException(status_code=500, detail=f"Module with this title already exists")

    return {
        "message" : "Module create success",
        "data" : create_module
    }


@router.put("/{id}")
async def update_module(
    id: int,
    course_id: Annotated[int, Form()] = None,
    title: Annotated[str, Form()] = None,
    description: Annotated[str, Form()] = None,
    position: Annotated[int, Form()] = None,
    created_at: Annotated[int, Form()] = None, 
    files: Optional[List[UploadFile]] = File(None)                            
):
    if files:
        result = check_image_formant(files)

        if not result:
            raise HTTPException(status_code=500, detail={
                    "status": "error",
                    "msg": f"All image must be in png/jpg/jpeg format"
                })
    
    module = Module(id=id, course_id=course_id, title=title, description=description, position=position, created_at=created_at)

    result = module_repository.update_module(id, module, files)

    if not result:
        raise HTTPException(status_code=404, detail=f"Module with id {id} or course with id {module.course_id} not found")

    return  {
        "message" : f"Module with id {id} update success",
        "data" : result
    }


@router.delete("/{id}")
async def delete_module(id: int):
    result = module_repository.delete_module_by_id(id)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Module with id {id} not found")

    return {"message" : "Module delete success"}