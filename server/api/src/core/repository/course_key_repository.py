from src.core.database.database import db
from src.core.models.models import CourseKey
from config import Config
from src.core.repository import course_repository

config = Config()

def get_all_course_keys():
    query = "SELECT * FROM Course_keys"
    course_keys = db.fetch_all(query)

    if course_keys:
        for course_key in course_keys:
            course_key['course_data'] = course_repository.get_simple_course_by_id_with_color_config_and_images(course_key['course_id'])
            
            del course_key['user_id']
            del course_key['course_id']

    return course_keys


def get_course_key_by_id(id: int):
    query = "SELECT * FROM Course_keys WHERE id=%s"
    course_key = db.fetch_one(query, (id,))

    if course_key:
        course_key['course_data'] = course_repository.get_simple_course_by_id_with_color_config_and_images(course_key['course_id'])
        
        del course_key['user_id']
        del course_key['course_id']

    return course_key


def get_course_key_by_course_id(course_id: int,):
    query = "SELECT * FROM Course_keys WHERE course_id=%s"
    course_keys = db.fetch_all(query, (course_id,))

    if course_keys:
        for course_key in course_keys:
            course_key['course_data'] = course_repository.get_simple_course_by_id_with_color_config_and_images(course_key['course_id'])
            
            del course_key['user_id']
            del course_key['course_id']
            
    return course_keys


def create_course_key(course_key: CourseKey):
    check_course_exist = course_repository.get_simple_cours_by_id(course_key.course_id)
    
    if not check_course_exist:
        return False
    
    query = ("INSERT INTO Course_keys (user_id, course_id) VALUES (%s, %s)")
    params = (course_key.user_id, course_key.course_id)

    cursor = db.execute_query(query, params)
    
    return get_course_key_by_id(cursor.lastrowid)


def delete_course_key_by_id(id: int):
    check_course_key_exist = get_course_key_by_id(id)

    if not check_course_key_exist:
        return False

    query = "DELETE FROM Course_keys WHERE id=%s"
    db.execute_query(query, (id,))

    return True
