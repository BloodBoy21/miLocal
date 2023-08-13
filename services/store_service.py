from fastapi import HTTPException, status
from models.store import StoreWithUser, StoreOut, StoreIn
from repositories.store_repository import StoreRepository
from models.user import User

store_repository = StoreRepository()


def create_store(store: StoreIn, user: User) -> StoreOut:
    if store_repository.exists(store.address):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Store already exists",
        )
    store_with_user = StoreWithUser(**store.dict(), user_id=user.user_id)
    store_data = store_repository.create(store_with_user)
    store_out = StoreOut(**store_data.__dict__)
    return store_out


def get_user_stores(user: User) -> list[StoreOut]:
    stores = store_repository.find_by_user_id(user.user_id)
    return [StoreOut(**store.__dict__) for store in stores]
