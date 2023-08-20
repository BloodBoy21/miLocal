from pydantic import BaseModel, Field
from database.mongo import database
from datetime import datetime
from typing import Optional

PRODUCTS_COLLECTION = database.get_collection("products")


class Product(BaseModel):
    name: str = Field(...)
    description: str = Field(default="")
    sku: str = Field(...)
    price: float = Field(...)
    stock: int = Field(...)
    store_id: int = Field(..., index=True)
    created_at: str = datetime.now()
    updated_at: str = datetime.now()


class ProductIn(BaseModel):
    name: str = Field(...)
    description: str = Field(default="")
    sku: str = Field(...)
    price: float = Field(...)
    stock: int = Field(...)
    stores: list[int] = Field(...)
    store_id: Optional[int]


class ProductOut(ProductIn):
    _id: str
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


class ProductDelete(BaseModel):
    stores: list[int]


class ProductDeleteMany(BaseModel):
    ids: list[str]
