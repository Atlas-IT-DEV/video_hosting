from typing import Annotated, List, Optional
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, Depends, Request
from src.core.repository import course_repository
from src.core.models.models import Course
from src.utils.file_operation import check_image_formant
from src.secure.main_secure import role_required
from src.secure.secure_entity import Role
from minio import Minio
import subprocess
import os
import aiofiles


router = APIRouter(
    prefix="/api/courses",
    tags=["Courses CRUD"],
)

# Подключение к MinIO
minio_client = Minio(
    "127.0.0.1:9000",  # Укажите адрес MinIO
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)
BUCKET_NAME = "videohosting.videos"



@router.get("/")
async def get_courses(secure_data: dict = Depends(role_required(Role.USER))):
    page = course_repository.get_all_courses()
    return page


@router.get("/{id}")
async def get_course_by_id(id: int, secure_data: dict = Depends(role_required(Role.USER))):
    course = course_repository.get_course_by_id(id)
    
    if not course:
        raise HTTPException(status_code=404, detail=f"Course with id {id} not found")
    
    return course


@router.get("/title/{title}")
async def get_course_by_title(title: str, secure_data: dict = Depends(role_required(Role.USER))):
    course = course_repository.get_course_by_title(title)
    
    if not course:
        raise HTTPException(status_code=404, detail=f"Course with title {title} not found")
    
    return course


@router.post("/")
async def create_course(
    color_config_id: Annotated[int, Form()] = None,
    title: Annotated[str, Form()] = None,
    description: Annotated[str, Form()] = None,
    created_at: Annotated[int, Form()] = None, 
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
    
    course = Course(id=id, color_config_id=color_config_id, title=title, description=description, created_at=created_at)

    result = course_repository.update_course(id, course, files)

    if not result:
        raise HTTPException(status_code=404, detail=f"Course with id {id} or color config with id {course.color_config_id} not found")

    return  {
        "message" : f"Course with id {id} update success",
        "data" : result
    }
@router.post("/video/upload")
async def upload_video(file: UploadFile = File(...)):
    """Загрузка видео в MinIO и конвертация в HLS"""
    file_path = f"temp/{file.filename}"
    hls_path = f"temp/hls/{file.filename.split('.')[0]}"
    
    # Сохраняем временный файл
    os.makedirs("temp", exist_ok=True)
    os.makedirs("temp/hls", exist_ok=True)
    async with aiofiles.open(file_path, "wb") as out_file:
        while content := await file.read(1024 * 1024):  # Читаем кусками по 1MB
            await out_file.write(content)
    
    # Конвертация в HLS
    os.makedirs(hls_path, exist_ok=True)
    command = [
        "ffmpeg", "-i", file_path, "-profile:v", "baseline", "-level", "3.0",
        "-start_number", "0", "-hls_time", "10", "-hls_list_size", "0",
        "-f", "hls", f"{hls_path}/index.m3u8"
    ]
    subprocess.run(command, check=True)
    
    # Загрузка HLS в MinIO
    for f in os.listdir(hls_path):
        minio_client.fput_object(BUCKET_NAME, f"hls/{file.filename.split('.')[0]}/{f}", f"{hls_path}/{f}")
    
    # Удаление временных файлов
    os.remove(file_path)
    
    return {"message": "Video uploaded and converted to HLS", "video_id": file.filename.split('.')[0]}

@router.post("/video/octet/upload")
async def upload_video(request: Request):
    """Загрузка видео в MinIO и конвертация в HLS"""
    
    # Получаем название файла из заголовка запроса
    filename = request.headers.get("X-Filename", "video.mp4")  
    video_id = filename.split('.')[0]

    # Пути
    file_path = f"temp/{filename}"
    hls_path = f"temp/hls/{video_id}"

    # Создаем папки, если их нет
    os.makedirs("temp", exist_ok=True)
    os.makedirs("temp/hls", exist_ok=True)

    # Читаем бинарные данные и записываем в файл
    async with aiofiles.open(file_path, "wb") as out_file:
        while chunk := await request.stream().__anext__():  
            await out_file.write(chunk)

    # Конвертация в HLS
    os.makedirs(hls_path, exist_ok=True)
    command = [
        "ffmpeg", "-i", file_path, "-profile:v", "baseline", "-level", "3.0",
        "-start_number", "0", "-hls_time", "10", "-hls_list_size", "0",
        "-f", "hls", f"{hls_path}/index.m3u8"
    ]
    subprocess.run(command, check=True)

    # Загрузка HLS в MinIO
    for f in os.listdir(hls_path):
        minio_client.fput_object(BUCKET_NAME, f"hls/{video_id}/{f}", f"{hls_path}/{f}")

    # Удаление временного файла
    os.remove(file_path)

    return {"message": "Video uploaded and converted to HLS", "video_id": video_id}

@router.get("/video/stream/{video_id}")
def get_hls(video_id: str):
    """Возвращает ссылку на HLS плейлист"""
    hls_url = f"http://me-course.com:9000/{BUCKET_NAME}/hls/{video_id}/index.m3u8"
    return {"hls_url": hls_url}


@router.delete("/{id}")
async def delete_course(id: int, secure_data: dict = Depends(role_required(Role.MANAGER))):
    result = course_repository.delete_course_by_id(id)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Course with id {id} not found")

    return {"message" : "Course delete success"}