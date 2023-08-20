from fastapi import APIRouter, Depends
from utils.middlware_wrapper import create_middleware_wrapper

from middleware.store_middleware import store_owner
from middleware.product_middleware import product_owner_by_id
import services.product_service as product_service
from utils.auth import auth_user
from models.user import User
from models.mongo.product import (
    ProductIn,
    ProductUpdate,
    ProductDelete,
    ProductDeleteMany,
)

router = APIRouter()
is_store_owner = create_middleware_wrapper(callback=store_owner)
is_product_owner = create_middleware_wrapper(callback=product_owner_by_id)


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


@router.delete("/many")
@is_product_owner
async def delete_products(
    products: ProductDeleteMany = None,
    ids: list[str] = [],
    user: User = Depends(auth_user),
) -> dict:
    return await product_service.delete_many_products(ids)


@router.delete("/{sku}")
@is_store_owner
async def delete_product(
    sku: str, product: ProductDelete, user: User = Depends(auth_user)
) -> dict:
    return await product_service.delete_product(sku, product)
