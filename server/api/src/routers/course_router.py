from typing import Annotated, List, Optional
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from src.core.repository import course_repository
from src.core.models.models import Course
from src.utils.file_operation import check_image_formant


router = APIRouter(
    prefix="/api/courses",
    tags=["Courses CRUD"],
)


@router.get("/")
async def get_courses():
    page = course_repository.get_all_courses()
    return page


@router.get("/{id}")
async def get_course_by_id(id: int):
    course = course_repository.get_course_by_id(id)
    
    if not course:
        raise HTTPException(status_code=404, detail=f"Course with id {id} not found")
    
    return course


@router.post("/")
async def create_course(
    color_config_id: Annotated[int, Form()] = None,
    title: Annotated[str, Form()] = None,
    description: Annotated[str, Form()] = None,
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
        
    course = Course(id=0, color_config_id=color_config_id, title=title, description=description, created_at=created_at)

    create_course = course_repository.create_course(course, files)

    if not create_course:
        raise HTTPException(status_code=500, detail=f"Course with this title already exists")

    return {
        "message" : "Course create success",
        "data" : create_course
    }


@router.put("/{id}")
async def update_course(
    id: int,
    color_config_id: Annotated[int, Form()] = None,
    title: Annotated[str, Form()] = None,
    description: Annotated[str, Form()] = None,
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
    
    course = Course(id=id, color_config_id=color_config_id, title=title, description=description, created_at=created_at)

    result = course_repository.update_course(id, course, files)

    if not result:
        raise HTTPException(status_code=404, detail=f"Course with id {id} or color config with id {course.color_config_id} not found")

    return  {
        "message" : f"Course with id {id} update success",
        "data" : result
    }


@router.delete("/{id}")
async def delete_course(id: int):
    result = course_repository.delete_course_by_id(id)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Course with id {id} not found")

    return {"message" : "Course delete success"}