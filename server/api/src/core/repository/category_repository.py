from src.database.my_connector import db
from src.database.models import Categories


def get_all_categories():
    query = "SELECT * FROM categories"
    return db.fetch_all(query)


def get_category_by_id(category_id: int):
    query = "SELECT * FROM categories WHERE id=%s"
    return db.fetch_one(query, (category_id,))


def create_category(category: Categories):
    query = "INSERT INTO categories (name) VALUES (%s)"
    params = category.Name
    cursor = db.execute_query(query, params)
    return cursor.lastrowid


def update_category(category_id: int, category: Categories):
    query = "UPDATE categories SET name=%s WHERE id=%s"
    params = category.Name, category_id
    db.execute_query(query, params)


def delete_category(category_id: int):
    query = "DELETE FROM categories WHERE id=%s"
    db.execute_query(query, (category_id,))
