from fastapi import HTTPException, status
from fastapi.exceptions import HTTPException
from bson.objectid import ObjectId
from models.mongo.product import ProductIn
from repositories.store_repository import StoreRepository
from models.user import User

store_repository = StoreRepository()


async def store_owner(product: ProductIn, user: User, **kwargs):
    product.store_id = (
        product.store_id if isinstance(product.store_id, list) else [product.store_id]
    )
    for store_id in product.store_id:
        store = store_repository.find_by_id(store_id)
        if store is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Store not found",
            )
        if store.user_id != user.user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )
    return
