from fastapi import HTTPException, status
from models.mongo.product import ProductIn
from repositories.product_repository import ProductRepository
from models.user import User

product_repository = ProductRepository()


async def create_product(product: ProductIn) -> dict:
    existing_product = await product_repository.exists(product.sku)
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product already exists",
        )
    new_product = await product_repository.create(product)
    return {"product_id": str(new_product.inserted_id)}
