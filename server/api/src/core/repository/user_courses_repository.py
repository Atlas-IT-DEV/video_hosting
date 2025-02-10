from src.core.database.database import db
from src.core.models.models import UserCourse
from config import Config
from src.core.repository import course_repository, user_repository

config = Config()

def get_all_user_courses():
    query = "SELECT * FROM User_Courses"
    user_courses = db.fetch_all(query)

    if user_courses:
        for user_course in user_courses:
            user_course['user_data'] = user_repository.get_simple_user_by_id(user_course['user_id'])
            user_course['course_data'] = course_repository.get_simple_course_by_id_with_color_config_and_images(user_course['course_id'])
            
            del user_course['user_id']
            del user_course['course_id']

    return user_courses


def get_user_course_by_id(id: int):
    query = "SELECT * FROM User_Courses WHERE id=%s"
    user_course = db.fetch_one(query, (id,))

    if user_course:
        user_course['user_data'] = user_repository.get_simple_user_by_id(user_course['user_id'])
        user_course['course_data'] = course_repository.get_simple_course_by_id_with_color_config_and_images(user_course['course_id'])
        
        del user_course['user_id']
        del user_course['course_id']

    return user_course


def get_user_course_by_user_id(user_id: int):
    query = "SELECT * FROM User_Courses WHERE user_id=%s"
    user_courses = db.fetch_all(query, (user_id,))

    if user_courses:
        for user_course in user_courses:
            user_course['user_data'] = user_repository.get_simple_user_by_id(user_course['user_id'])
            user_course['course_data'] = course_repository.get_simple_course_by_id_with_color_config_and_images(user_course['course_id'])
            
            del user_course['user_id']
            del user_course['course_id']
        
    return user_courses


def get_simple_user_course_by_user_id(user_id: int):
    query = "SELECT * FROM User_Courses WHERE user_id=%s"
    user_courses = db.fetch_all(query, (user_id,))

    if user_courses:
        for user_course in user_courses:
            user_course['course_data'] = course_repository.get_simple_course_by_id_with_color_config_and_images(user_course['course_id'])
            
            del user_course['user_id']
            del user_course['course_id']
        
    return user_courses


def get_user_course_by_course_id(course_id: int,):
    query = "SELECT * FROM User_Courses WHERE course_id=%s"
    user_courses = db.fetch_all(query, (course_id,))

    if user_courses:
        for user_course in user_courses:
            user_course['user_data'] = user_repository.get_simple_user_by_id(user_course['user_id'])
            user_course['course_data'] = course_repository.get_simple_course_by_id_with_color_config_and_images(user_course['course_id'])
            
            del user_course['user_id']
            del user_course['course_id']
            
    return user_courses


def create_user_course(user_course: UserCourse):
    check_user_exist = user_repository.get_simple_user_by_id(user_course.user_id)
    
    if not check_user_exist:
        return False
    
    check_course_exist = course_repository.get_simple_cours_by_id(user_course.course_id)
    
    if not check_course_exist:
        return False
    
    query = ("INSERT INTO User_Courses (user_id, course_id) VALUES (%s, %s)")
    params = (user_course.user_id, user_course.course_id)

    cursor = db.execute_query(query, params)
    
    return get_user_course_by_id(cursor.lastrowid)


def delete_user_course_by_id(id: int):
    check_user_course_exist = get_user_course_by_id(id)

    if not check_user_course_exist:
        return False

    query = "DELETE FROM User_Courses WHERE id=%s"
    db.execute_query(query, (id,))

    return True
