import shutil
import os
import shortuuid

from fastapi import UploadFile

def get_unique_short_uuid4() -> str:
    return shortuuid.uuid()


def upload_file(path: str, file: UploadFile, filename: str) -> str | None:
    if not file or not filename:
        return None

    path_model, path_field = path.split('/')
    if path_model not in os.listdir("public"):
        os.mkdir(f"public/{path_model}")
        os.mkdir(f"public/{path_model}/{path_field}")

    unique_name = str(get_unique_short_uuid4())
    os.mkdir(f"public/{path}/{unique_name}")
    location = f"public/{path}/{unique_name}/{filename}"

    with open(location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    return location


def delete_file(path: str):
    if path:
        directory = '/'.join(path.split('/')[:-1])
        os.remove(path)
        if not os.listdir(directory):
            os.rmdir(directory)
            

def get_file_format(file: UploadFile) -> str:
    return file.filename.split('.')[-1]
