from src.core.database.database import db
from src.core.models.models import Image, ImageLevelEnum
from config import Config

config = Config()

def get_all_images():
    query = "SELECT * FROM Images"
    images = db.fetch_all(query)

    if images:
        for image in images:
            image['full_path'] = f"{config.__getattr__("PROTOCOL")}://{config.__getattr__("HOST")}:{config.__getattr__("SERVER_PORT")}/{image['path']}"

    return images


def get_image_by_id(image_id: int):
    query = "SELECT * FROM Images WHERE id=%s"
    image = db.fetch_one(query, (image_id,))

    if image:
        image['full_path'] = f"{config.__getattr__("PROTOCOL")}://{config.__getattr__("HOST")}:{config.__getattr__("SERVER_PORT")}/{image['path']}"

    return image


def get_image_by_object_id_and_type(object_id: int, type: str):
    query = "SELECT * FROM Images WHERE object_id=%s AND type=%s GROUP BY level, position ORDER BY level DESC, position ASC"
    images = db.fetch_all(query, (object_id, type,))

    if images:
        for image in images:
            image['full_path'] = f"{config.__getattr__("PROTOCOL")}://{config.__getattr__("HOST")}:{config.__getattr__("SERVER_PORT")}/{image['path']}"

    return images


def create_image(image: Image):
    query = ("INSERT INTO Images (type, level, position, object_id, path) VALUES (%s, %s, %s, %s, %s)")
    params = (image.type, image.level, image.position, image.object_id, image.path)

    cursor = db.execute_query(query, params)
    
    return get_image_by_id(cursor.lastrowid)


def create_single_image(image: Image, file):
    from src.utils.file_operation import download_file_for_entity

    image.path = download_file_for_entity(image.object_id, image.type, [file], image.level, False)

    check_main_image_exist(image.object_id, image.type, image.level)

    query = ("INSERT INTO Images (type, level, position, object_id, path) VALUES (%s, %s, %s, %s, %s)")
    params = (image.type, image.level, image.position, image.object_id, image.path)

    cursor = db.execute_query(query, params)
    
    return get_image_by_id(cursor.lastrowid)


def update_image(id: int, image: Image):
    try:
        check_image_exist = get_image_by_id(id)

        if not check_image_exist:
            return False

        query = "UPDATE Images SET type=%s, level=%s, position=%s, object_id=%s, path=%s WHERE id=%s"
        params = (image.type, image.level, image.position, image.object_id, image.path, id)
        
        db.execute_query(query, params)

        return get_image_by_id(id)
    except:
        return False
    

def update_image_level_and_position(id: int, level: str, position: int):
    try:
        check_image_exist = get_image_by_id(id)

        if not check_image_exist:
            return False
        
        check_main_image_exist(check_image_exist['object_id'], check_image_exist['type'], level)

        query = "UPDATE Images SET level=%s, position=%s WHERE id=%s"
        params = (level, position, id)
        
        db.execute_query(query, params)

        return get_image_by_id(id)
    except:
        return False


def delete_image_by_id(id: int):
    check_image_exist = get_image_by_id(id)

    if not check_image_exist:
        return False

    query = "DELETE FROM Images WHERE id=%s"
    db.execute_query(query, (id,))

    return True


def delete_image_by_object_id_and_type(id, type):
    query = "DELETE FROM Images WHERE object_id=%s AND type=%s"
    db.execute_query(query, (id, type,))

    return True


def delete_single_image_by_id(id):
    from src.utils.file_operation import delete_file

    image = get_image_by_id(id)

    if not image:
        return False

    query = "DELETE FROM Images WHERE id=%s"
    db.execute_query(query, (id,))

    delete_file(image['path'])

    return True


def check_main_image_exist(object_id, type, new_level, only_create = True):
    if new_level == ImageLevelEnum.MAIN:
        query = "SELECT * FROM Images WHERE object_id=%s AND type=%s AND level=%s"
        cur_main_image = db.fetch_one(query, (object_id, type, new_level,))

        if cur_main_image:
            query = "UPDATE Images SET level=%s WHERE id=%s"
            params = (ImageLevelEnum.ADDITIONAL, cur_main_image['id'])
            db.execute_query(query, params)
