from src.core.database.database import db
from src.core.models.models import Course
from src.core.repository.config_color_repository import get_config_color_by_id
from src.utils.file_operation import delete_file_for_entity, download_file_for_entity
from src.core.repository import images_repository, module_repository

def get_all_courses():
    query = "SELECT * FROM Courses"
    courses = db.fetch_all(query)

    if courses:
        for course in courses:
            course['color_config'] = get_config_color_by_id(course['color_config_id'])
            del course['color_config_id']

            course['images'] = images_repository.get_image_by_object_id_and_type(course['id'], 'course')
            course['modules'] = module_repository.get_all_modules_by_course_id(course['id'])

    return courses


def get_course_by_id(course_id: int, user_id: str = None):
    query = "SELECT * FROM Courses WHERE id=%s"
    course = db.fetch_one(query, (course_id,))

    if course:
        course['color_config'] = get_config_color_by_id(course['color_config_id'])
        del course['color_config_id']

        course['images'] = images_repository.get_image_by_object_id_and_type(course_id, 'course')
        course['modules'] = module_repository.get_all_modules_by_course_id(course_id, user_id)

    return course


def get_simple_course_by_id_with_color_config_and_images(course_id: int):
    query = "SELECT * FROM Courses WHERE id=%s"
    course = db.fetch_one(query, (course_id,))

    if course:
        course['color_config'] = get_config_color_by_id(course['color_config_id'])
        course['images'] = images_repository.get_image_by_object_id_and_type(course_id, 'course')
        
        del course['color_config_id']

    return course


def get_course_by_title(title: str):
    query = "SELECT * FROM Courses WHERE title=%s"
    course = db.fetch_one(query, (title,))

    if course:
        course['color_config'] = get_config_color_by_id(course['color_config_id'])
        del course['color_config_id']

        course['images'] = images_repository.get_image_by_object_id_and_type(course['id'], 'course')
        course['modules'] = module_repository.get_all_modules_by_course_id(course['id'])

    return course


def get_simple_cours_by_id(course_id):
    query = "SELECT * FROM Courses WHERE id=%s"
    return db.fetch_one(query, (course_id,)) 


def create_course(course: Course, files = []):
    result_check = get_course_by_title(course.title)

    if result_check:
        return False
    
    if course.color_config_id:
        result_check = get_config_color_by_id(course.color_config_id)

        if not result_check:
            return False

    query = ("INSERT INTO Courses (color_config_id, title, description, created_at)"
             " VALUES (%s, %s, %s, %s)")
    
    params = (course.color_config_id, course.title, course.description, course.created_at)
    
    cursor = db.execute_query(query, params)

    if files and len(files):
        download_file_for_entity(cursor.lastrowid, 'course', files)

    return get_course_by_id(cursor.lastrowid)


def update_course(id: int, course: Course, files = []):
    try:
        check_course_exist = get_course_by_id(id)

        if not check_course_exist:
            return False
    
        if course.color_config_id:
            check_config_color_exist = get_config_color_by_id(course.color_config_id)

            if not check_config_color_exist:
                return False

        query = "UPDATE Courses SET color_config_id=%s, title =%s, description=%s, created_at=%s WHERE id=%s"
        params = (course.color_config_id, course.title, course.description, course.created_at, id)
        
        db.execute_query(query, params)

        if files and len(files):
            delete_file_for_entity(id, 'course')
            download_file_for_entity(id, 'course', files)

        return get_course_by_id(id)
    except:
        return False


def delete_course_by_id(id: int):
    check_course_exist = get_course_by_id(id)

    if not check_course_exist:
        return False

    query = "DELETE FROM Courses WHERE id=%s"
    db.execute_query(query, (id,))

    # delete files and folder
    delete_file_for_entity(id, 'course')

    return True
