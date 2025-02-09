from src.core.database.database import db
from src.core.models.models import Image

def get_all_images():
    query = "SELECT * FROM Images"
    return db.fetch_all(query)


def get_image_by_id(image_id: int):
    query = "SELECT * FROM Images WHERE id=%s"
    return db.fetch_one(query, (image_id,))


def get_image_by_object_id_and_type(object_id: int, type: str):
    query = "SELECT * FROM Images WHERE object_id=%s AND type=%s"
    return db.fetch_all(query, (object_id, type,))


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
