from fastapi import HTTPException, status
from fastapi.exceptions import HTTPException
from models.mongo.product import ProductDeleteMany
from repositories.product_repository import ProductRepository
from models.user import User
from repositories.store_repository import StoreRepository
from bson import ObjectId

product_repository = ProductRepository()
store_repository = StoreRepository()


async def product_owner_by_id(ids: list[str], user: User, **kwargs):
    products_ids = [ObjectId(product_id) for product_id in ids]
    user_stores = store_repository.find_by_user_id(user.user_id)
    user_stores = [store.store_id for store in user_stores]
    pipeline = [
        {
            "$match": {
                "store_id": {"$in": user_stores},
                "_id": {"$in": products_ids},
            }
        },
        {
            "$group": {
                "_id": "products",
                "product_ids": {"$addToSet": "$_id"},
            }
        },
        {"$project": {"_id": 0, "product_ids": 1}},
    ]
    results = product_repository.aggregation(pipeline)
    matching_product_ids = await results.to_list(length=None)
    if len(matching_product_ids) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Products not found",
        )
    matching_product_ids = matching_product_ids[0]["product_ids"]
    return {
        "ids": matching_product_ids,
    }
