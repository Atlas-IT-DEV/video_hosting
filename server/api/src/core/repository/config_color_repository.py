from src.core.database.database import db
from src.core.models.models import ColorConfig
import re


def get_all_config_colors():
    query = "SELECT * FROM Color_config"
    #TODO getted images
    return db.fetch_all(query)


def get_config_color_by_id(config_color_id: int):
    query = "SELECT * FROM Color_config WHERE id=%s"
    #TODO getted images
    return db.fetch_one(query, (config_color_id,))


def create_config_color(config_color: ColorConfig):
    query = ("INSERT INTO Color_config (custom_color_1,	custom_color_2, custom_color_3, custom_color_4, custom_color_5)"
             " VALUES (%s, %s, %s, %s, %s)")
    
    params = (config_color.custom_color_1, config_color.custom_color_2, config_color.custom_color_3, config_color.custom_color_4, config_color.custom_color_5)
    
    all_color_is_hex_color = True
    
    for color in params:
        match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color)

        if not match:                      
            all_color_is_hex_color = False
            break
        
    if not all_color_is_hex_color:
        return False
    
    #TODO loaded images 
    
    cursor = db.execute_query(query, params)
    return cursor.lastrowid


def update_config_color(id: int, config_color: ColorConfig):
    try:
        check_config_color_exist = get_config_color_by_id(id)

        if not check_config_color_exist:
            return False

        query = "UPDATE Color_config SET custom_color_1=%s, custom_color_2 =%s, custom_color_3=%s, custom_color_4=%s, custom_color_5=%s WHERE id=%s"
        params = (config_color.custom_color_1, config_color.custom_color_2, config_color.custom_color_3, config_color.custom_color_4, config_color.custom_color_5, id)
        
        db.execute_query(query, params)
        
        #TODO updated images 

        return get_config_color_by_id(config_color.id)
    except:
        return False


def delete_config_color_by_id(id: int):
    check_config_color_exist = get_config_color_by_id(id)

    if not check_config_color_exist:
        return False
    
    #TODO deleted images 

    query = "DELETE FROM Color_config WHERE id=%s"
    db.execute_query(query, (id,))

    return True
