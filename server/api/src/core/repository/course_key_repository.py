from src.core.database.database import db
from src.core.models.models import CourseKey, CourseKeyStatusEnum, UserCourse
from config import Config
from src.core.repository import course_repository, user_repository, user_courses_repository
import time
import hashlib

config = Config()

def get_all_course_keys():
    query = "SELECT * FROM Course_keys"
    return db.fetch_all(query)


def get_all_course_keys_was_activate(course_id: int):
    query = "SELECT * FROM Course_keys WHERE course_id=%s AND status=%s"
    return db.fetch_all(query, (course_id, CourseKeyStatusEnum.INACTIVE))


def get_all_course_keys_was_not_activate(course_id: int):
    query = "SELECT * FROM Course_keys WHERE course_id=%s AND status=%s"
    return db.fetch_all(query, (course_id, CourseKeyStatusEnum.ACTIVE))


def get_course_keys_by_id(id: int):
    query = "SELECT * FROM Course_keys WHERE id=%s"
    return db.fetch_one(query, (id,))


def get_course_keys_by_course_id(course_id: int):
    query = "SELECT * FROM Course_keys WHERE course_id=%s"
    return db.fetch_all(query, (course_id,))


def get_course_keys_by_text_key(text_key: str):
    query = "SELECT * FROM Course_keys WHERE text_key=%s"
    return db.fetch_one(query, (text_key,))


def create_course_key(course_key: CourseKey):
    check_course_exist = course_repository.get_simple_cours_by_id(course_key.course_id)
    
    if not check_course_exist:
        return False
    
    timestamp = str(time.time()).encode('utf-8')
    hashed_timestamp = hashlib.sha256(timestamp).hexdigest()

    course_key.text_key = f"{hashed_timestamp}{course_key.course_id}"
    
    query = ("INSERT INTO Course_keys (text_key, course_id) VALUES (%s, %s)")
    params = (course_key.text_key, course_key.course_id)

    cursor = db.execute_query(query, params)
    
    return get_course_keys_by_id(cursor.lastrowid)


def activate_course_key(user_id: int, text_key: str):
    check_user_exist = user_repository.get_simple_user_by_id(user_id)
    
    if not check_user_exist:
        return False

    course_key = get_course_keys_by_text_key(text_key)
    
    if not course_key:
        return False
    
    if course_key['status'] == CourseKeyStatusEnum.INACTIVE:
        return False
    
    query = ("UPDATE Course_keys SET status=%s WHERE id=%s")
    params = (CourseKeyStatusEnum.INACTIVE, course_key['id'])
    cursor = db.execute_query(query, params)

    if cursor:
        return user_courses_repository.create_user_course(UserCourse(id=0, user_id=user_id, course_id=int(course_key['course_id'])))
    
    return False


def delete_course_key_by_id(id: int):
    check_course_key_exist = get_course_keys_by_id(id)

    if not check_course_key_exist:
        return False

    query = "DELETE FROM Course_keys WHERE id=%s"
    db.execute_query(query, (id,))

    return True


def delete_course_key_by_text_key(text_key: str):
    check_course_key_exist = get_course_keys_by_text_key(text_key)

    if not check_course_key_exist:
        return False

    query = "DELETE FROM Course_keys WHERE text_key=%s"
    db.execute_query(query, (text_key,))

    return True
