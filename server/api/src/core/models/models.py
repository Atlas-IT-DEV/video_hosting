from pydantic import BaseModel


# class CharacteristicTypeEnum(StrictStr, Enum):
#     """
#     Model of characteristic types
#     """
#     Int = 'INT'
#     Varchar = 'VARCHAR'
#     Boolean = 'BOOLEAN'
#     Float = 'FLOAT'
#     Text = 'TEXT'
#     TimeStamp = 'TIMESTAMP'
#     Decimal = 'DECIMAL'
#     Json = 'JSON'


# class ImageTypeEnum(StrictStr, Enum):
#     """
#     Model of product image types
#     """
#     Main = 'main'
#     Additional = 'additional'


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



# class ProductImages(BaseModel):
#     """
#     Model of product images
#     """
#     ID: Optional[int] = Field(None,
#                                 alias="id")
#     ProductID: StrictInt = Field(...,
#                                 alias="product_id",
#                                 examples=[2],
#                                 description="Product ID of product")
#     ImageID: StrictInt = Field(...,
#                                 alias="image_id",
#                                 examples=[2],
#                                 description="Image ID of product")
#     ImageType: ImageTypeEnum = Field(...,
#                                 alias="image_type",
#                                 examples=[ImageTypeEnum.Main],
#                                 description="Image type")
#     Color: Optional[StrictStr] = Field(None,
#                                         alias="color",
#                                         examples=["Красный"],
#                                         description="Color of product")


# class Favorite(BaseModel):
#     """
#     Model of favorite
#     """
#     ID: Optional[int] = Field(None,
#                               alias="id")
#     UserID: int = Field(...,
#                         alias="user_id",
#                         examples=[10],
#                         description="User ID")
#     ProductID: int = Field(...,
#                            alias="product_id",
#                            examples=[12],
#                            description="Product ID")


# class CommentImages(BaseModel):
#     """
#     Model of comment images
#     """
#     ID: Optional[int] = Field(None,
#                               alias="id")
#     CommentID: StrictInt = Field(...,
#                                  alias="comment_id",
#                                  examples=[2],
#                                  description="Comment ID of comment")
#     ImageID: StrictInt = Field(...,
#                                alias="image_id",
#                                examples=[2],
#                                description="Image ID of comment")