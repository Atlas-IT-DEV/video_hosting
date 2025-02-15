from src.core.database.database import db
from src.core.models.models import User
from src.core.repository.common_tools import checkEntityAlreadyExists
from src.core.repository import user_courses_repository


def get_all_users():
    query = "SELECT * FROM Users"
    return db.fetch_all(query)


def get_user_by_id(user_id: int):
    query = "SELECT * FROM Users WHERE id=%s"
    user = db.fetch_one(query, (user_id,))
    
    if user:
        user['curses'] = user_courses_repository.get_simple_user_course_by_user_id(user_id)
    
    return user


def get_simple_user_by_id(user_id: int):
    query = "SELECT * FROM Users WHERE id=%s"
    return db.fetch_one(query, (user_id,))


def get_user_by_email(email: str):
    query = "SELECT * FROM Users WHERE email=%s"
    user = db.fetch_one(query, (email,))
    
    if user:
        user['curses'] = user_courses_repository.get_simple_user_course_by_user_id(user['id'])
    
    return user


def get_user_by_phone(phone: str):
    query = "SELECT * FROM Users WHERE phone=%s"
    user = db.fetch_one(query, (phone,))
    
    if user:
        user['curses'] = user_courses_repository.get_simple_user_course_by_user_id(user['id'])
    
    return user


def create_user(user: User):
    result_check = checkEntityAlreadyExists('user', user)

    if not result_check:
        return False

    query = ("INSERT INTO Users (id, email, avatar_url, first_name, last_name, country, phone, role, additional_data)"
             " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
    
    params = (user.id, user.email, user.avatar_url, user.first_name, user.last_name,
              user.country, user.phone, user.role, user.additional_data)
    
    cursor = db.execute_query(query, params)

    return get_user_by_id(user.id)


def update_user(id: int, user: User):
    try:
        check_user_exist = get_user_by_id(id)

        if not check_user_exist:
            return False

        query = "UPDATE Users SET "
        params = ()

        if user.email:
            query += "email=%s, "
            params = params + (user.email,)


        if user.avatar_url:
            query += "avatar_url=%s, "
            params = params + (user.avatar_url,)

        if user.first_name:
            query += "first_name=%s, "
            params = params + (user.first_name,)

        if user.last_name:
            query += "last_name=%s, "
            params = params + (user.last_name,)

        if user.country:
            query += "country=%s, "
            params = params + (user.country,)

        if user.phone:
            query += "phone=%s, "
            params = params + (user.phone,)

        if user.role:
            query += "role=%s, "
            params = params + (user.role,)

        if user.additional_data:
            query += "additional_data=%s, "
            params = params + (user.additional_data,)

        query = query[:-2]

        query += " WHERE id=%s"
        params = params + (id,)
        
        db.execute_query(query, params)

        return get_user_by_id(id)
    except:
        return False


def delete_user_by_id(id: int):
    check_user_exist = get_user_by_id(id)

    if not check_user_exist:
        return False

    query = "DELETE FROM Users WHERE id=%s"
    db.execute_query(query, (id,))

    return True
