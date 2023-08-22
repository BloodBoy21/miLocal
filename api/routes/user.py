from fastapi import APIRouter, Depends
from models.user import UserIn, UserLogin, User
from models.store import StoreOut
import services.user_service as user_service
import services.store_service as store_service
from utils.auth import auth_user

router = APIRouter()


@router.post("/register")
def create_user(user: UserIn) -> dict:
    return user_service.create_user(user)


@router.get("/stores")
def create_store(user: User = Depends(auth_user)) -> list[StoreOut]:
    return store_service.get_user_stores(user)


@router.post("/login")
def login_user(user: UserLogin) -> dict:
    return user_service.login_user(user)
