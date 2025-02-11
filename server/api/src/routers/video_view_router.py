from fastapi import APIRouter, HTTPException
from src.core.repository import video_view_repository
from src.core.models.models import VideoView
import typing

router = APIRouter(
    prefix="/api/users/video/views",
    tags=["Video views CRUD"],
)


@router.get("/")
async def get_video_views():
    page = video_view_repository.get_all_video_views()
    return page


@router.get("/common/{id}")
async def get_video_view_by_id(id: int):
    video_view = video_view_repository.get_video_view_by_id(id)
    
    if not video_view:
        raise HTTPException(status_code=404, detail=f"Video view with id {id} not found")
    
    return video_view


@router.get("/user/{id}")
async def get_video_view_by_user_id(user_id: int):
    video_views = video_view_repository.get_video_view_by_user_id(user_id)
    
    if not video_views:
        raise HTTPException(status_code=404, detail=f"Video view with user id {user_id} not found")
    
    return video_views

@router.get("/module/{id}")
async def get_video_view_by_module_id(module_id: int):
    video_views = video_view_repository.get_video_view_by_module_id(module_id)
    
    if not video_views:
        raise HTTPException(status_code=404, detail=f"Video view with module id {module_id} not found")
    
    return video_views


@router.get("/course/{id}")
async def get_video_view_by_course_id(course_id: int):
    video_views = video_view_repository.get_video_view_by_course_id(course_id)
    
    if not video_views:
        raise HTTPException(status_code=404, detail=f"Video view with course id {course_id} not found")
    
    return video_views


@router.post("/")
async def create_video_view(video_view: VideoView):
    create_video_view = video_view_repository.create_video_view(VideoView(**video_view.model_dump()))

    if not create_video_view:
        raise HTTPException(status_code=500, detail=f"Something data by id not found")

    return {
        "message" : "Video view create success",
        "data" : create_video_view
    }


@router.delete("/{id}")
async def delete_video_view(id: int):
    result = video_view_repository.delete_video_view_by_id(id)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Video view with id {id} not found")

    return {"message" : "Video view delete success"}