from src.core.models.models import User
from src.core.repository import user_repository

def checkEntityAlreadyExists(entity_type, data):

    if entity_type == 'user':
        
        result = user_repository.get_user_by_id(data.id)

        if result:
            return False
        
        result = user_repository.get_user_by_email(data.email)

        if result:
            return False
        
        result = user_repository.get_user_by_phone(data.phone)

        if result:
            return False

    return True