from pydantic import BaseModel, Field
from database.mongo import database
from datetime import datetime

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
    store_id: int = Field(...)
