from models.mongo.product import Product, ProductIn
from repositories.repository_mongo import RepositoryMongo
from models.mongo.product import Product


class ProductRepository(RepositoryMongo):
    def __init__(self):
        super().__init__(Product, "products")

    async def create(self, product: ProductIn):
        product_data = self.model(**product.dict())
        return await super().create(product_data)

    async def exists(self, sku: str, store_id: str) -> bool:
        return await self.find_one({"sku": sku, "store_id": store_id}) is not None
