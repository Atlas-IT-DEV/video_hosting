from typing import Annotated, List, Optional
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, Depends, Request, Query
from fastapi.responses import StreamingResponse
from src.core.repository import course_repository
from src.core.models.models import Course
from src.utils.file_operation import check_image_formant
from src.secure.main_secure import role_required
from src.secure.secure_entity import Role
from src.core.repository import video_repository
from src.core.repository import module_repository
from src.core.repository import course_repository
from minio import Minio
from src.core.repository.user_repository import get_user_by_id
import subprocess
import os
import aiofiles
import hashlib
from datetime import datetime
import json
import os
import uuid
from fastapi import HTTPException
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix="/api/courses",
    tags=["Courses CRUD"],
)

# Подключение к MinIO
minio_client = Minio(
    "me-course.com:9500",  # Укажите адрес MinIO
    access_key="admin",
    secret_key="secretpassword",
    secure=True
)
BUCKET_NAME = "videohosting"



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
    creator_id: Annotated[str, Form()] = None,
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
        
    course = Course(id=0, color_config_id=color_config_id, title=title, description=description, created_at=created_at, creator_id=creator_id)

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
    creator_id: Annotated[str, Form()] = None,
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
    
    course = Course(id=id, color_config_id=color_config_id, title=title, description=description, created_at=created_at, creator_id=creator_id)

    result = course_repository.update_course(id, course, files)

    if not result:
        raise HTTPException(status_code=404, detail=f"Course with id {id} or color config with id {course.color_config_id} not found")

    return  {
        "message" : f"Course with id {id} update success",
        "data" : result
    }
@router.post("/video/upload")
async def upload_video(user_id: str = Query(..., description="ID пользователя")):
    """Генерация presigned URL для загрузки видео."""
    unique_string = f"{user_id}_{datetime.now().timestamp()}"
    hashed = hashlib.sha256(unique_string.encode()).hexdigest()
    object_name = f"videos/{user_id}/{hashed}.mp4"
    
    presigned_url = minio_client.presigned_put_object(BUCKET_NAME, object_name)
    
    return {"upload_url": presigned_url, "video_id": hashed, "object_name": object_name}

@router.post("/video/process")
async def process_video(object_name: str = Query(..., description="MinIO object name"), user_id: str = Query(..., description="ID пользователя")):
    """Загрузка видео из MinIO, конвертация в HLS и загрузка обратно."""
    hashed = object_name.split("/")[-1].replace(".mp4", "")
    file_path = f"temp/{user_id}/{hashed}.mp4"
    hls_path = f"temp/{user_id}/hls/{hashed}"
    os.makedirs(hls_path, exist_ok=True)
    
    # Скачивание видео из MinIO
    minio_client.fget_object(BUCKET_NAME, object_name, file_path)
    
    # Конвертация в HLS
    command = [
        "ffmpeg", "-i", file_path, "-profile:v", "baseline", "-level", "3.0",
        "-start_number", "0", "-hls_time", "10", "-hls_list_size", "0",
        "-f", "hls", f"{hls_path}/index.m3u8"
    ]
    subprocess.run(command, check=True)
    
    # Загрузка HLS в MinIO
    for f in os.listdir(hls_path):
        minio_client.fput_object(
            BUCKET_NAME,
            f"hls/{user_id}/{hashed}/{f}",
            f"{hls_path}/{f}"
        )
    
    # Удаление временных файлов
    os.remove(file_path)
    
    return {"message": "Video processed and converted to HLS", "hls_url": f"hls/{user_id}/{hashed}/index.m3u8"}

# @router.get("/video/stream/{video_id}")
# def get_hls(video_id: str):
#     """Возвращает ссылку на HLS плейлист, ищет во всех папках бакета"""
#     try:
#         # Ищем все объекты в бакете, которые содержат video_id
#         objects = minio_client.list_objects(BUCKET_NAME, prefix="hls/", recursive=True)
        
#         # Ищем объект, который соответствует video_id и является плейлистом HLS
#         hls_playlist = None
#         for obj in objects:
#             if obj.object_name.endswith(f"{video_id}/index.m3u8"):
#                 hls_playlist = obj.object_name
#                 break
        
#         if not hls_playlist:
#             raise HTTPException(status_code=404, detail="Video not found")
        
#         # Формируем URL для HLS плейлиста
#         hls_url = f"https://me-course.com:9500/{BUCKET_NAME}/{hls_playlist}"
#         return {"hls_url": hls_url}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@router.get("/video/stream/{video_id}/{user_id}")
def get_mp4_from_hls(video_id: str, user_id: str):
    """Отдаёт MP4-видео с водяным знаком, преобразованное из HLS"""
    try:
        user = get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail=f"User with id {id} not found")
        # Ищем HLS-плейлист в MinIO
        objects = minio_client.list_objects(BUCKET_NAME, prefix="hls/", recursive=True)
        hls_playlist = next(
            (obj.object_name for obj in objects if obj.object_name.endswith(f"{video_id}/index.m3u8")), None
        )

        if not hls_playlist:
            raise HTTPException(status_code=404, detail="HLS-видео не найдено")

        # Получаем временную ссылку на HLS-плейлист из MinIO
        hls_url = minio_client.presigned_get_object(BUCKET_NAME, hls_playlist)


        # Базовые параметры отрисовки текста
        font_size = 24
        font_color = "green"
        x_position = "10"
        y_start = 50  # Начальная позиция Y
        line_spacing = 30  # Расстояние между строками
        json_data = '{"Имя": "Иван", "Возраст": "30", "Город": "Москва"}'
        data = json.loads(user['additional_data'])

        # Генерируем drawtext фильтры для каждого ключа-значения
        drawtext_filters = []
        for i, (key, value) in enumerate(data.items()):
            y_position = y_start + i * line_spacing
            drawtext_filters.append(
                f"drawtext=text='{key}: {value}':fontsize={font_size}:fontcolor={font_color}:x={x_position}:y={y_position}"
            )

        # Объединяем фильтры через запятую
        filter_complex = ",".join(drawtext_filters)

        # Формируем команду FFmpeg
        command = [
            "ffmpeg",
            "-i", hls_url,  # Входной HLS-поток
            "-vf", filter_complex,  # Фильтр с текстом
            "-c:v", "libx264",  # Кодек видео
            "-profile:v", "main",  # Используем основной профиль H.264
            "-pix_fmt", "yuv420p",  # Формат пикселей для совместимости
            "-c:a", "aac",  # Кодек аудио
            "-b:a", "128k",  # Битрейт аудио (128 kbps)
            "-f", "mp4",  # Формат вывода — MP4
            "-movflags", "frag_keyframe+empty_moov",  # Прогрессивный MP4
            "pipe:1"  # Вывод в stdout
        ]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Возвращаем потоковое видео с заголовком о длительности
        return StreamingResponse(
            process.stdout,
            media_type="video/mp4",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@router.get("/testvideo/stream/{video_id}/{user_id}")
def get_mp4_from_hls(video_id: str, user_id: str):
    """Генерирует MP4-видео с водяным знаком и возвращает ссылку на файл"""
    try:
        user = get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail=f"User with id {id} not found")
        
        # Ищем HLS-плейлист в MinIO
        objects = minio_client.list_objects(BUCKET_NAME, prefix="hls/", recursive=True)
        hls_playlist = next(
            (obj.object_name for obj in objects if obj.object_name.endswith(f"{video_id}/index.m3u8")), None
        )

        if not hls_playlist:
            raise HTTPException(status_code=404, detail="HLS-видео не найдено")

        # Получаем временную ссылку на HLS-плейлист из MinIO
        hls_url = minio_client.presigned_get_object(BUCKET_NAME, hls_playlist)

        # Базовые параметры отрисовки текста
        font_size = 24
        font_color = "green"
        x_position = "10"
        y_start = 50  # Начальная позиция Y
        line_spacing = 30  # Расстояние между строками
        data = json.loads(user['additional_data'])

        # Генерируем drawtext фильтры для каждого ключа-значения
        drawtext_filters = []
        for i, (key, value) in enumerate(data.items()):
            y_position = y_start + i * line_spacing
            drawtext_filters.append(
                f"drawtext=text='{key}: {value}':fontsize={font_size}:fontcolor={font_color}:x={x_position}:y={y_position}"
            )

        # Объединяем фильтры через запятую
        filter_complex = ",".join(drawtext_filters)

        # Генерируем уникальное имя для временного файла
        temp_file = f"/tmp/{uuid.uuid4()}.mp4"

        # Формируем команду FFmpeg
        command = [
            "ffmpeg",
            "-i", hls_url,  # Входной HLS-поток
            "-vf", filter_complex,  # Фильтр с текстом
            "-c:v", "libx264",  # Кодек видео
            "-profile:v", "main",  # Используем основной профиль H.264
            "-pix_fmt", "yuv420p",  # Формат пикселей для совместимости
            "-c:a", "aac",  # Кодек аудио
            "-b:a", "128k",  # Битрейт аудио (128 kbps)
            "-f", "mp4",  # Формат вывода — MP4
            temp_file  # Сохраняем в временный файл
        ]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print("FFmpeg error:", stderr.decode())
            raise HTTPException(status_code=500, detail="Ошибка обработки видео")

        # Загружаем сгенерированный файл в MinIO
        output_file_name = f"videos/{video_id}_{user_id}.mp4"
        with open(temp_file, "rb") as file:
            minio_client.put_object(BUCKET_NAME, output_file_name, file, os.path.getsize(temp_file))

        # Удаляем временный файл
        os.remove(temp_file)

        # Возвращаем ссылку на файл
        file_url = minio_client.presigned_get_object(BUCKET_NAME, output_file_name)
        return JSONResponse(content={"url": file_url})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/video/user-videos")
def get_user_videos(user_id: str = Query(..., description="ID пользователя")):
    """Возвращает список всех видео пользователя"""
    # Получаем список объектов в каталоге пользователя
    objects = minio_client.list_objects(BUCKET_NAME, prefix=f"hls/{user_id}/", recursive=True)
    total_size = 0

    # Получаем все видео из репозитория
    videos = video_repository.get_all_videos()
    videos_info = []  # Список для хранения информации о видео

    # Формируем список видео
    for obj in objects:
        total_size += obj.size
        if obj.object_name.endswith(".m3u8"):
            video_id = obj.object_name.split("/")[2]  # Извлекаем ID видео
            video_url = f"https://me-course.com:9500/{BUCKET_NAME}/{obj.object_name}"

            # Ищем информацию о видео с соответствующим video_id
            video_info = {}
            for video in videos:
                if video["video_url"] == video_id:
                    video_info = video  # Если нашли, добавляем информацию о видео
                    video_info['module'] = module_repository.get_module_by_id(video_info['module_id'])
                    video_info['course'] = course_repository.get_course_by_id(video_info['module']['course_id'])


            # Добавляем информацию о видео в список
            videos_info.append({
                "video_id": video_id,
                "hls_url": video_url,
                "last_modified": obj.last_modified.isoformat(), 
                "video_info": video_info  # Добавляем всю информацию о видео, если она найдена
            })
    
    return {"videos": videos_info, "total_size": total_size}


@router.delete("/{id}")
async def delete_course(id: int, secure_data: dict = Depends(role_required(Role.MANAGER))):
    result = course_repository.delete_course_by_id(id)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Course with id {id} not found")

    return {"message" : "Course delete success"}