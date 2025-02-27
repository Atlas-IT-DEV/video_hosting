import shutil
import os
import shortuuid
from pathlib import Path
from fastapi import UploadFile

from src.core.models.models import Image
from src.core.repository import images_repository

def get_unique_short_uuid4() -> str:
    return shortuuid.uuid()


def upload_file(path: str, file: UploadFile, entity_id: int) -> str | None:
    if not file or not entity_id:
        return None

    # path_model, path_field = path.split('/')

    path_model = path

    # if path_model not in os.listdir("public"):
    # os.mkdir(f"public/{path_model}")
    # os.mkdir(f"public/{path_model}/{entity_id}")

    Path(f"public/{path_model}/{entity_id}").mkdir(parents=True, exist_ok=True)
    
        # os.mkdir(f"public/{path_model}/{path_field}")

    unique_name = str(get_unique_short_uuid4())
    # os.mkdir(f"public/{path}/{unique_name}")
    file_format = get_file_format(file)
    location = f"public/{path}/{entity_id}/{unique_name}.{file_format}"

    with open(location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    return location


def delete_file(path: str):
    try:
        if path:
            directory = '/'.join(path.split('/')[:-1])
            os.remove(path)
            if not os.listdir(directory):
                os.rmdir(directory)
    except:
        pass
            

def get_file_format(file: UploadFile) -> str:
    return file.filename.split('.')[-1]

def check_image_formant(files):
    for file in files:
        if get_file_format(file) not in ['png', 'jpg', 'jpeg', 'webp', 'pdf', 'docx', 'text']:
            return False
    return True


# universal download files
def download_file_for_entity(object_id, type, files, level = "M", create_mode = True):
    for index, file in enumerate(files):
        new_upload_file_path = upload_file(type, file, object_id)

        if not create_mode:
            return new_upload_file_path

        # additional type images
        if index != 0:
            level = "A"
        
        new_image = Image(id=0, type=type, level=level, position=(index+1), object_id=object_id, path=new_upload_file_path)
        images_repository.create_image(new_image)


# universal delete files
def delete_file_for_entity(id, type):
    images = images_repository.get_image_by_object_id_and_type(id, type)
    
    images_repository.delete_image_by_object_id_and_type(id, type)

    if images:
        for image in images:
            delete_file(image['path'])

