from fastapi import APIRouter, HTTPException, Depends
from src.core.repository import course_key_repository
from src.core.models.models import CourseKey
from src.secure.main_secure import role_required
from src.secure.secure_entity import Role


router = APIRouter(
    prefix="/api/course/key",
    tags=["Course keys CRUD"],
)


@router.get("/")
async def get_all_course_keys(secure_data: dict = Depends(role_required(Role.MANAGER))):
    page = course_key_repository.get_all_course_keys()
    return page


@router.get("/was/activated")
async def get_all_course_keys_was_activate(course_id: int, secure_data: dict = Depends(role_required(Role.MANAGER))):
    course_key_courses = course_key_repository.get_all_course_keys_was_activate(course_id)
    
    if not course_key_courses:
        raise HTTPException(status_code=404, detail=f"Course key was activated with course id {course_id} not found")
    
    return course_key_courses


@router.get("/not/was/activated")
async def get_all_course_keys_was_not_activate(course_id: int, secure_data: dict = Depends(role_required(Role.MANAGER))):
    course_key_courses = course_key_repository.get_all_course_keys_was_not_activate(course_id)
    
    if not course_key_courses:
        raise HTTPException(status_code=404, detail=f"Course key not was activated with course id {course_id} not found")
    
    return course_key_courses


@router.get("/{id}")
async def get_course_keys_by_id(id: int, secure_data: dict = Depends(role_required(Role.MANAGER))):
    course_key_courses = course_key_repository.get_course_keys_by_id(id)
    
    if not course_key_courses:
        raise HTTPException(status_code=404, detail=f"Course key with id {id} not found")
    
    return course_key_courses


@router.get("/text/{text_key}")
async def get_course_keys_by_text_key(text_key: str, secure_data: dict = Depends(role_required(Role.MANAGER))):
    course_key_courses = course_key_repository.get_course_keys_by_text_key(text_key)
    
    if not course_key_courses:
        raise HTTPException(status_code=404, detail=f"Course key with text key {text_key} not found")
    
    return course_key_courses


@router.get("/course/{course_id}")
async def get_course_keys_by_course_id(course_id: int, secure_data: dict = Depends(role_required(Role.MANAGER))):
    course_key_courses = course_key_repository.get_course_keys_by_course_id(course_id)
    
    if not course_key_courses:
        raise HTTPException(status_code=404, detail=f"Course key with id {id} not found")
    
    return course_key_courses


@router.post("/")
async def create_course_key(course_key_course: CourseKey, secure_data: dict = Depends(role_required(Role.MANAGER))):
    create_course_key = course_key_repository.create_course_key(CourseKey(**course_key_course.model_dump()))

    if not create_course_key:
        raise HTTPException(status_code=500, detail=f"Course with id {course_key_course.course_id} not found")

    return {
        "message" : "Course key create success",
        "data" : create_course_key
    }


@router.post("/activate")
async def activate_course_key(user_id: int, text_key: str, secure_data: dict = Depends(role_required(Role.USER))):
    activate_course_key = course_key_repository.activate_course_key(user_id, text_key)

    if not activate_course_key:
        raise HTTPException(status_code=500, detail=f"User with id {user_id} or key {text_key} not found")

    return {
        "message" : "Course key activate success",
        "data" : activate_course_key
    }


@router.delete("/{id}")
async def delete_course_key_by_id(id: int, secure_data: dict = Depends(role_required(Role.MANAGER))):
    result = course_key_repository.delete_course_key_by_id(id)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Course key with id {id} not found")

    return {"message" : "Course key delete success"}


@router.delete("/text/key")
async def delete_course_key_by_text_key(text_key: str, secure_data: dict = Depends(role_required(Role.MANAGER))):
    result = course_key_repository.delete_course_key_by_text_key(text_key)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Course key with text key {text_key} not found")

    return {"message" : "Course key delete success"}
