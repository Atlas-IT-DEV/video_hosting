from fastapi import APIRouter, HTTPException, Depends
from src.core.repository import user_courses_repository
from src.core.models.models import UserCourse
from src.secure.main_secure import role_required
from src.secure.secure_entity import Role


router = APIRouter(
    prefix="/api/users/curses",
    tags=["User courses CRUD"],
)


@router.get("/")
async def get_user_courses(secure_data: dict = Depends(role_required(Role.USER))):
    page = user_courses_repository.get_all_user_courses()
    return page


@router.get("/common/{id}")
async def get_user_course_by_id(id: int, secure_data: dict = Depends(role_required(Role.USER))):
    user_course = user_courses_repository.get_user_course_by_id(id)
    
    if not user_course:
        raise HTTPException(status_code=404, detail=f"User course with id {id} not found")
    
    return user_course


@router.get("/user/{user_id}")
async def get_user_course_by_user_id(user_id: str, secure_data: dict = Depends(role_required(Role.USER))):
    user_courses = user_courses_repository.get_user_course_by_user_id(user_id)
    
    if not user_courses:
        raise HTTPException(status_code=404, detail=f"User course with user id {user_id} not found")
    
    return user_courses


@router.get("/course/{course_id}")
async def get_user_course_by_course_id(course_id: int, secure_data: dict = Depends(role_required(Role.USER))):
    user_courses = user_courses_repository.get_user_course_by_course_id(course_id)
    
    if not user_courses:
        raise HTTPException(status_code=404, detail=f"User course with course id {course_id} not found")
    
    return user_courses


@router.post("/")
async def create_user_course(user_course: UserCourse):
    if user_courses_repository.check_user_course_exists(user_course.user_id, user_course.course_id):
        return {
        "message" : "Epic fail",
        "details" : "we have someone also"
        }
    
    create_user_course = user_courses_repository.create_user_course(UserCourse(**user_course.model_dump()))

    if not create_user_course:
        raise HTTPException(status_code=500, detail=f"User with id {user_course.user_id} or course with id {user_course.course_id} not found")

    return {
        "message" : "User course create success",
        "data" : create_user_course
    }


@router.delete("/{id}")
async def delete_user_course(id: int, secure_data: dict = Depends(role_required(Role.MANAGER))):
    result = user_courses_repository.delete_user_course_by_id(id)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"User course with id {id} not found")

    return {"message" : "User course delete success"}