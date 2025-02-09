from src.core.database.database import db
from src.core.models.models import Module
from src.core.repository.config_color_repository import get_config_color_by_id
from src.utils.file_operation import delete_file_for_entity, download_file_for_entity
from src.core.repository import images_repository, course_repository, video_repository


def get_all_modules():
    query = "SELECT * FROM Modules"
    modules = db.fetch_all(query)

    if modules:
        for module in modules:
            module['videos'] = video_repository.get_all_videos_by_module_id(module['id'])
            module['images'] = images_repository.get_image_by_object_id_and_type(module['id'], 'module')

    return modules


def get_all_modules_by_course_id(course_id):
    query = "SELECT * FROM Modules WHERE course_id=%s ORDER BY position"
    modules = db.fetch_all(query, (course_id,))

    if modules:
        for module in modules:
            module['videos'] = video_repository.get_all_videos_by_module_id(module['id'])
            module['images'] = images_repository.get_image_by_object_id_and_type(module['id'], 'module')

    return modules


def get_module_by_id(module_id: int):
    query = "SELECT * FROM Modules WHERE id=%s"
    module = db.fetch_one(query, (module_id,))

    if module:
        module['videos'] = video_repository.get_all_videos_by_module_id(module_id)
        module['images'] = images_repository.get_image_by_object_id_and_type(module_id, 'module')

    return module


def get_simple_module_by_id(module_id):
    query = "SELECT * FROM Modules WHERE id=%s"
    return db.fetch_one(query, (module_id,))


def get_module_by_title(title: str):
    query = "SELECT * FROM Modules WHERE title=%s"
    module = db.fetch_one(query, (title,))

    if module:
        module['videos'] = video_repository.get_all_videos_by_module_id(module['id'])
        module['images'] = images_repository.get_image_by_object_id_and_type(module['id'], 'module')

    return module


def create_module(module: Module, files = []):
    result_check = get_module_by_title(module.title)

    if result_check:
        return False

    if module.course_id:
        result_check = course_repository.get_simple_cours_by_id(module.course_id)

        if not result_check:
            return False

    query = ("INSERT INTO Modules (course_id, title, description, position, created_at)"
             " VALUES (%s, %s, %s, %s, %s)")

    params = (module.course_id, module.title, module.description, module.position, module.created_at)

    cursor = db.execute_query(query, params)

    if files and len(files):
        download_file_for_entity(cursor.lastrowid, 'module', files)

    return get_module_by_id(cursor.lastrowid)


def update_module(id: int, module: Module, files = []):
    try:
        check_module_exist = get_module_by_id(id)

        if not check_module_exist:
            return False

        if module.course_id:
            check_course_exist = course_repository.get_simple_cours_by_id(module.course_id)

            if not check_course_exist:
                return False

        query = "UPDATE Modules SET course_id=%s, title =%s, description=%s, position=%s, created_at=%s WHERE id=%s"
        params = (module.course_id, module.title, module.description, module.position, module.created_at, id)

        db.execute_query(query, params)

        if files and len(files):
            delete_file_for_entity(id, 'module')
            download_file_for_entity(id, 'module', files)

        return get_module_by_id(id)
    except:
        return False


def delete_module_by_id(id: int):
    check_module_exist = get_module_by_id(id)

    if not check_module_exist:
        return False

    query = "DELETE FROM Modules WHERE id=%s"
    db.execute_query(query, (id,))

    # delete files and folder
    delete_file_for_entity(id, 'module')

    return True
