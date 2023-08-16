from fastapi import HTTPException, status
from models.mongo.product import ProductIn
from repositories.product_repository import ProductRepository
from models.user import User

product_repository = ProductRepository()


async def create_product(product: ProductIn) -> dict:
    products_created = []

    store_ids_to_process = list(product.store_id)

    for store_id in store_ids_to_process:
        remove_store = await product_repository.exists(product.sku, store_id)
        if remove_store:
            product.store_id.remove(store_id)
        else:
            temp_product = product
            temp_product.store_id = store_id
            new_product = await product_repository.create(temp_product)
            products_created.append(new_product)

    products_created_ids = [str(product.inserted_id) for product in products_created]
    if len(products_created_ids) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product already exists in all stores",
        )
    return {"products_id": products_created_ids}
