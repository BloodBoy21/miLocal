from fastapi import HTTPException, status
from models.mongo.product import (
    ProductIn,
    ProductOut,
    ProductUpdate,
    ProductDelete,
)
from repositories.product_repository import ProductRepository

product_repository = ProductRepository()


async def create_product(product: ProductIn) -> dict:
    products_created = []

    store_ids_to_process = product.stores

    for store_id in store_ids_to_process:
        remove_store = await product_repository.exists(product.sku, store_id)
        if remove_store:
            product.stores.remove(store_id)
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


async def get_product(product_id: str, store_id: int) -> ProductOut:
    product = await product_repository.get(product_id, store_id)
    if product:
        return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found",
    )


async def get_products(store_id: int) -> list[ProductOut]:
    products = await product_repository.get_by_store_id(store_id)
    products = [product async for product in products]
    if len(products) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Products not found",
        )
    products = [
        ProductOut(**product, product_id=product.get("_id")) for product in products
    ]
    return products


async def update_product(product: ProductUpdate, sku: str) -> dict:
    stores = product.stores
    product.stores = None
    product_data = product.dict(exclude_unset=True, exclude_none=True)
    data = await product_repository.update_many(
        {
            "sku": sku,
            "store_id": {"$in": stores},
        },
        {"$set": product_data},
    )
    if data.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Products not modified",
        )
    return {
        "sku": sku,
        "stores": stores,
    }


async def delete_product(sku: str, body: ProductDelete) -> dict:
    stores = body.stores
    data = await product_repository.delete_many(
        {"sku": sku, "store_id": {"$in": stores}}
    )
    if data.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product not deleted",
        )
    return {
        "sku": sku,
        "stores": stores,
    }


async def delete_many_products(ids: list[str]) -> dict:
    data = await product_repository.delete_many({"_id": {"$in": ids}})
    if data.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Products not deleted",
        )
    return {"products_id": [str(id) for id in ids]}
