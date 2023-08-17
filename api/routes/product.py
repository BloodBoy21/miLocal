from fastapi import APIRouter, Depends
from utils.middlware_wrapper import create_middleware_wrapper
from middleware.store_middleware import store_owner
import services.product_service as product_service
from utils.auth import auth_user
from models.user import User
from models.mongo.product import ProductIn, ProductUpdate, ProductDelete

router = APIRouter()
is_store_owner = create_middleware_wrapper(callback=store_owner)


@router.post("/")
@is_store_owner
async def create_product(
    user: User = Depends(auth_user), product: ProductIn = None
) -> dict:
    return await product_service.create_product(product)


@router.patch("/{sku}")
@is_store_owner
async def update_product(
    sku: str, product: ProductUpdate, user: User = Depends(auth_user)
) -> dict:
    return await product_service.update_product(product, sku)


@router.delete("/{sku}")
@is_store_owner
async def delete_product(
    sku: str, product: ProductDelete, user: User = Depends(auth_user)
) -> dict:
    return await product_service.delete_product(sku, product)
