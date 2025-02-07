from src.core.database.database import db
from src.core.models.models import User


def get_all_users():
    query = "SELECT * FROM Users"
    return db.fetch_all(query)


def get_user_by_id(user_id: int):
    query = "SELECT * FROM Users WHERE id=%s"
    return db.fetch_one(query, (user_id,))


def create_user(user: User):
    query = ("INSERT INTO Users (id, email, avatar_url, first_name, last_name, country, phone, role, additional_data)"
             " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
    
    params = (user.id, user.email, user.avatar_url, user.first_name, user.last_name,
              user.country, user.phone, user.role, user.additional_data)
    
    cursor = db.execute_query(query, params)
    return user.id


# def update_category(category_id: int, category: Categories):
#     query = "UPDATE categories SET name=%s WHERE id=%s"
#     params = category.Name, category_id
#     db.execute_query(query, params)


# def delete_category(category_id: int):
#     query = "DELETE FROM categories WHERE id=%s"
#     db.execute_query(query, (category_id,))
