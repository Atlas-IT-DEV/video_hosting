from fastapi import APIRouter, HTTPException
from src.core.repository import course_repository
from src.core.models.models import Course


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
async def create_course(course: Course):
    create_course = course_repository.create_course(Course(**course.model_dump()))

    if not create_course:
        raise HTTPException(status_code=500, detail=f"Course with this title already exists")

    return {
        "message" : "Course create success",
        "data" : create_course
    }


@router.put("/{id}")
async def update_course(id: int, course: Course):
    result = course_repository.update_course(id, course)

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