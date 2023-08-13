from repositories.repository import Repository
from models.store import Store, StoreWithUser


class StoreRepository(Repository):
    def __init__(self):
        super().__init__(Store)

    def find_by_id(self, store_id: int) -> Store:
        return self.find_query().filter_by(store_id=store_id).first()

    def create(self, store: StoreWithUser) -> Store:
        store_data = self.model(**store.dict())
        return super().create(store_data)

    def exists(self, address: str) -> bool:
        return self.find_query().filter_by(address=address).first() is not None

    def find_by_user_id(self, user_id: int) -> list[Store]:
        return self.find_query().filter_by(user_id=user_id).all()
