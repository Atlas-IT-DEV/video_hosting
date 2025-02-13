from pydantic import (BaseModel, Field, StrictStr, Json, condecimal,
                      StrictInt, PrivateAttr, SecretBytes, StrictBytes, StrictBool, model_validator)
from enum import Enum
from typing import Optional, List
from datetime import datetime
import os
from pathlib import Path


class CharacteristicTypeEnum(StrictStr, Enum):
    """
    Model of characteristic types
    """
    Int = 'INT'
    Varchar = 'VARCHAR'
    Boolean = 'BOOLEAN'
    Float = 'FLOAT'
    Text = 'TEXT'
    TimeStamp = 'TIMESTAMP'
    Decimal = 'DECIMAL'
    Json = 'JSON'


class ImageTypeEnum(StrictStr, Enum):
    """
    Model of product image types
    """
    Main = 'main'
    Additional = 'additional'


class Images(BaseModel):
    """
    Model of images
    """
    ID: Optional[int] = Field(None,
                              alias="id")
    Url: StrictStr = Field(...,
                           alias="url",
                           examples=["https://example.com"],
                           description="URL of images")


class ProductImages(BaseModel):
    """
    Model of product images
    """
    ID: Optional[int] = Field(None,
                                alias="id")
    ProductID: StrictInt = Field(...,
                                alias="product_id",
                                examples=[2],
                                description="Product ID of product")
    ImageID: StrictInt = Field(...,
                                alias="image_id",
                                examples=[2],
                                description="Image ID of product")
    ImageType: ImageTypeEnum = Field(...,
                                alias="image_type",
                                examples=[ImageTypeEnum.Main],
                                description="Image type")
    Color: Optional[StrictStr] = Field(None,
                                        alias="color",
                                        examples=["Красный"],
                                        description="Color of product")


class Favorite(BaseModel):
    """
    Model of favorite
    """
    ID: Optional[int] = Field(None,
                              alias="id")
    UserID: int = Field(...,
                        alias="user_id",
                        examples=[10],
                        description="User ID")
    ProductID: int = Field(...,
                           alias="product_id",
                           examples=[12],
                           description="Product ID")


class CommentImages(BaseModel):
    """
    Model of comment images
    """
    ID: Optional[int] = Field(None,
                              alias="id")
    CommentID: StrictInt = Field(...,
                                 alias="comment_id",
                                 examples=[2],
                                 description="Comment ID of comment")
    ImageID: StrictInt = Field(...,
                               alias="image_id",
                               examples=[2],
                               description="Image ID of comment")