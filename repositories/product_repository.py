from models.mongo.product import Product, ProductIn
from repositories.repository_mongo import RepositoryMongo
from models.mongo.product import Product
from models.store import StoreProductFilters


class ProductRepository(RepositoryMongo):
    def __init__(self):
        super().__init__(Product, "products")

    async def create(self, product: ProductIn):
        product_data = self.model(**product.dict())
        return await super().create(product_data)

    async def exists(self, sku: str, store_id: str) -> bool:
        return await self.find_one({"sku": sku, "store_id": store_id}) is not None

    async def get(self, product_id: str, store_id: int) -> Product:
        return await self.find_one({"_id": product_id, "store_id": store_id})

    async def get_by_store_id(
        self, store_id: int, filters: StoreProductFilters
    ) -> list[Product]:
        return await self.find_many({"store_id": store_id, **filters.__dict__})

    def update(self, query: dict, data: dict):
        return self.update_one(query, data)

    def update_many(self, query: dict, data: dict):
        return super().update_many(query, data)

    def delete_many(self, query: dict):
        return super().delete_many(query)
