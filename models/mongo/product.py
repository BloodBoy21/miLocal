from pydantic import BaseModel, Field
from database.mongo import database
from datetime import datetime
from typing import Optional
from bson.objectid import ObjectId as BsonObjectId

PRODUCTS_COLLECTION = database.get_collection("products")


class PydanticObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info):
        if not isinstance(v, BsonObjectId):
            raise TypeError("ObjectId required")
        return str(v)


class Product(BaseModel):
    name: str = Field(...)
    description: str = Field(default="")
    sku: str = Field(...)
    price: float = Field(...)
    stock: int = Field(...)
    image: str = Field(default="")
    store_id: int = Field(..., index=True)
    created_at: str = datetime.now()
    updated_at: str = datetime.now()


class ProductIn(BaseModel):
    name: str = Field(...)
    description: str = Field(default="")
    sku: str = Field(...)
    price: float = Field(...)
    stock: int = Field(...)
    stores: Optional[list[int]] = Field(default=None)
    store_id: Optional[int]
    image: Optional[str]


class ProductOut(ProductIn):
    product_id: PydanticObjectId
    store_id: int
    created_at: datetime
    updated_at: datetime


class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    sku: Optional[str]
    price: Optional[float]
    stock: Optional[int]
    stores: list[int]
    image: Optional[str]


class ProductDelete(BaseModel):
    stores: list[int]


class ProductDeleteMany(BaseModel):
    ids: list[str]
