from typing import Annotated, List, Optional
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from src.core.repository import video_repository
from src.core.models.models import Video
from src.utils.file_operation import check_image_formant


router = APIRouter(
    prefix="/api/videos",
    tags=["Videos CRUD"],
)


@router.get("/")
async def get_videos():
    page = video_repository.get_all_videos()
    return page


@router.get("/{id}")
async def get_video_by_id(id: int):
    video = video_repository.get_video_by_id(id)
    
    if not video:
        raise HTTPException(status_code=404, detail=f"Video with id {id} not found")
    
    return video


@router.post("/")
async def create_video(
    module_id: Annotated[int, Form()] = None,
    title: Annotated[str, Form()] = None,
    description: Annotated[str, Form()] = None,
    position: Annotated[int, Form()] = None,
    video_url: Annotated[str, Form()] = None,
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
        
    video = Video(id=0, module_id=module_id, title=title, description=description, video_url=video_url, position=position, created_at=created_at)

    create_video = video_repository.create_video(video, files)

    if not create_video:
        raise HTTPException(status_code=500, detail=f"Video with this title already exists")

    return {
        "message" : "Video create success",
        "data" : create_video
    }


@router.put("/{id}")
async def update_video(
    id: int,
    module_id: Annotated[int, Form()] = None,
    title: Annotated[str, Form()] = None,
    description: Annotated[str, Form()] = None,
    position: Annotated[int, Form()] = None,
    video_url: Annotated[str, Form()] = None,
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
    
    video = Video(id=id, module_id=module_id, title=title, description=description, video_url=video_url, position=position, created_at=created_at)

    result = video_repository.update_video(id, video, files)

    if not result:
        raise HTTPException(status_code=404, detail=f"Video with id {id} or module with id {video.module_id} not found")

    return  {
        "message" : f"Video with id {id} update success",
        "data" : result
    }


@router.delete("/{id}")
async def delete_video(id: int):
    result = video_repository.delete_video_by_id(id)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Video with id {id} not found")

    return {"message" : "Video delete success"}