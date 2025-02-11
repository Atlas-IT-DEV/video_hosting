from src.core.database.database import db
from src.core.models.models import VideoView
from config import Config
from src.core.repository import module_repository, video_repository, user_repository

config = Config()

def get_all_video_views():
    query = "SELECT * FROM Video_Views"
    return db.fetch_all(query)


def get_video_view_by_id(id: int):
    query = "SELECT * FROM Video_Views WHERE id=%s"
    return db.fetch_one(query, (id,))


def get_video_view_by_user_id(user_id: int):
    query = "SELECT * FROM Video_Views WHERE user_id=%s"
    return db.fetch_all(query, (user_id,))


def get_video_view_by_video_id(video_id: int):
    query = "SELECT * FROM Video_Views WHERE video_id=%s"
    return db.fetch_all(query, (video_id,))


def get_video_view_by_module_id(module_id: int,):
    query = "SELECT * FROM Video_Views WHERE module_id=%s"
    return db.fetch_all(query, (module_id,))


def get_video_view_by_course_id(course_id: int,):
    query = "SELECT * FROM Video_Views WHERE course_id=%s"
    return db.fetch_all(query, (course_id,))


def create_video_view(video_view: VideoView):
    check_user_exist = user_repository.get_simple_user_by_id(video_view.user_id)
    
    if not check_user_exist:
        return False

    check_video_exist = video_repository.get_video_by_id(video_view.video_id)
    
    if not check_video_exist:
        return False

    cur_module = module_repository.get_simple_module_by_id(check_video_exist['module_id'])

    video_view.module_id = check_video_exist['module_id']
    video_view.course_id = cur_module['course_id']
    
    query = ("INSERT INTO Video_Views (user_id, course_id, module_id, video_id) VALUES (%s, %s, %s, %s)")
    params = (video_view.user_id, video_view.course_id, video_view.module_id, video_view.video_id)

    cursor = db.execute_query(query, params)
    
    return get_video_view_by_id(cursor.lastrowid)


def delete_video_view_by_id(id: int):
    check_video_view_exist = get_video_view_by_id(id)

    if not check_video_view_exist:
        return False

    query = "DELETE FROM Video_Views WHERE id=%s"
    db.execute_query(query, (id,))

    return True
