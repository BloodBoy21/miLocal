from fastapi import APIRouter, Depends
from utils.auth import auth_user
from models.store import StoreIn, StoreOut, StoreProductFilters
import services.store_service as store_service
from models.user import User, UserLocation
import services.product_service as product_service
from models.mongo.product import ProductOut
from typing import Optional

router = APIRouter()


@router.post("/")
def create_store(store: StoreIn, user: User = Depends(auth_user)) -> StoreOut:
    return store_service.create_store(store, user)


@router.get("/nearby")
def get_nearby_stores(lat: float, lon: float) -> list[StoreOut]:
    location = UserLocation(lat=lat, lon=lon)
    return store_service.get_nearby_stores(location)


@router.get("/{store_id}")
def get_store(store_id: int) -> StoreOut:
    return store_service.get_store(store_id)


@router.get("/{store_id}/products")
async def get_products(store_id: int, sale: Optional[bool] = False) -> list[ProductOut]:
    filters = StoreProductFilters(sale=sale)
    return await product_service.get_products(store_id, filters=filters)


@router.get("/{store_id}/product/{product_id}")
async def get_product(product_id: str, store_id) -> list[ProductOut]:
    return await product_service.get_product(product_id, store_id)
