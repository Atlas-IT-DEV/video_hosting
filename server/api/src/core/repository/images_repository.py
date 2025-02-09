from src.core.database.database import db
from src.core.models.models import Image
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
    query = "SELECT * FROM Images WHERE object_id=%s AND type=%s"
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
