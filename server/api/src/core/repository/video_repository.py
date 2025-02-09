from src.core.database.database import db
from src.core.models.models import Video
from src.core.repository.config_color_repository import get_config_color_by_id
from src.utils.file_operation import delete_file_for_entity, download_file_for_entity
from src.core.repository import images_repository, module_repository


def get_all_videos():
    query = "SELECT * FROM Videos"
    videos = db.fetch_all(query)

    if videos:
        for video in videos:
            video['images'] = images_repository.get_image_by_object_id_and_type(video['id'], 'video')

    return videos


def get_all_videos_by_module_id(module_id):
    query = "SELECT * FROM Videos WHERE module_id=%s ORDER BY position"
    videos = db.fetch_all(query, (module_id,))

    if videos:
        for video in videos:
            video['images'] = images_repository.get_image_by_object_id_and_type(video['id'], 'video')

    return videos


def get_video_by_id(module_id: int):
    query = "SELECT * FROM Videos WHERE id=%s"
    video = db.fetch_one(query, (module_id,))

    if video:
        video['images'] = images_repository.get_image_by_object_id_and_type(module_id, 'video')

    return video


def get_video_by_title(title: str):
    query = "SELECT * FROM Videos WHERE title=%s"
    video = db.fetch_one(query, (title,))

    if video:
        video['images'] = images_repository.get_image_by_object_id_and_type(video['id'], 'video')

    return video


def create_video(video: Video, files = []):
    result_check = get_video_by_title(video.title)

    if result_check:
        return False

    if video.module_id:
        result_check = module_repository.get_simple_module_by_id(video.module_id)

        if not result_check:
            return False

    query = ("INSERT INTO Videos (module_id, title, description, video_url, position, created_at)"
             " VALUES (%s, %s, %s, %s, %s, %s)")

    params = (video.module_id, video.title, video.description, video.video_url, video.position, video.created_at)

    cursor = db.execute_query(query, params)

    if files and len(files):
        download_file_for_entity(cursor.lastrowid, 'video', files)

    return get_video_by_id(cursor.lastrowid)


def update_video(id: int, video: Video, files = []):
    try:
        check_video_exist = get_video_by_id(id)

        if not check_video_exist:
            return False

        if video.module_id:
            check_video_exist = module_repository.get_simple_module_by_id(video.module_id)

            if not check_video_exist:
                return False

        query = "UPDATE Videos SET module_id=%s, title =%s, description=%s, video_url=%s, position=%s, created_at=%s WHERE id=%s"
        params = (video.module_id, video.title, video.description,  video.video_url, video.position, video.created_at, id)

        db.execute_query(query, params)

        if files and len(files):
            delete_file_for_entity(id, 'video')
            download_file_for_entity(id, 'video', files)

        return get_video_by_id(id)
    except:
        return False


def delete_video_by_id(id: int):
    check_video_exist = get_video_by_id(id)

    if not check_video_exist:
        return False

    query = "DELETE FROM Videos WHERE id=%s"
    db.execute_query(query, (id,))

    # delete files and folder
    delete_file_for_entity(id, 'video')

    return True
