from enum import Enum
from pydantic import BaseModel, StrictStr


class User(BaseModel):
    id: int
    email: str | None
    avatar_url: str | None
    first_name: str | None
    last_name: str | None
    country: str | None
    phone: str | None
    role: str | None
    additional_data: str | None
    

class ColorConfig(BaseModel):
    id: int
    custom_color_1: str | None
    custom_color_2: str | None
    custom_color_3: str | None
    custom_color_4: str | None
    custom_color_5: str | None


class Image(BaseModel):
    id: int
    type: str
    level: str
    position: int	
    object_id: int
    path: str


class Course(BaseModel):
    id: int
    color_config_id: int | None
    title: str | None
    description: str | None
    created_at: int | None


class Module(BaseModel):
    id: int
    course_id: int | None
    title: str | None
    description: str | None
    position: int | None
    created_at: int | None


class Video(BaseModel):
    id: int
    module_id: int | None
    title: str | None
    description: str | None
    position: int | None
    video_url: str | None
    created_at: int | None
    
    
class UserCourse(BaseModel):
    id: int
    user_id: int
    course_id: int


class CourseKey(BaseModel):
    id: int
    text_key: str = "need_change"
    course_id: int
    status: str = "A"


class VideoView(BaseModel):
    id: int
    user_id: int
    video_id: int
    module_id: int | None
    course_id: int | None


class CourseKeyStatusEnum(StrictStr, Enum):
    ACTIVE = 'A'
    INACTIVE = 'I'


class ImageLevelEnum(StrictStr, Enum):
    MAIN = 'M'
    ADDITIONAL = 'A'
