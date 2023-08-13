from fastapi import APIRouter, Depends
from utils.auth import auth_user
from models.store import StoreIn, StoreOut
import services.store_service as store_service
from models.user import User

router = APIRouter()


@router.post("/")
def create_store(store: StoreIn, user: User = Depends(auth_user)) -> StoreOut:
    return store_service.create_store(store, user)
