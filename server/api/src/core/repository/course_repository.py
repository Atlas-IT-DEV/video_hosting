from src.core.database.database import db
from src.core.models.models import Course
from src.core.repository.config_color_repository import get_config_color_by_id


def get_all_courses():
    query = "SELECT * FROM Courses"
    courses = db.fetch_all(query)

    if courses:
        for course in courses:
            course['color_config'] = get_config_color_by_id(course['color_config_id'])
            del course['color_config_id']

    return courses


def get_course_by_id(course_id: int):
    query = "SELECT * FROM Courses WHERE id=%s"
    course = db.fetch_one(query, (course_id,))

    if course:
        course['color_config'] = get_config_color_by_id(course['color_config_id'])
        del course['color_config_id']

    return course


def get_course_by_title(title: str):
    query = "SELECT * FROM Courses WHERE title=%s"
    course = db.fetch_one(query, (title,))

    if course:
        course['color_config'] = get_config_color_by_id(course['color_config_id'])
        del course['color_config_id']

    return course


def create_course(course: Course):
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

    return get_course_by_id(cursor.lastrowid)


def update_course(id: int, course: Course):
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

        return get_course_by_id(id)
    except:
        return False


def delete_course_by_id(id: int):
    check_course_exist = get_course_by_id(id)

    if not check_course_exist:
        return False

    query = "DELETE FROM Courses WHERE id=%s"
    db.execute_query(query, (id,))

    return True
