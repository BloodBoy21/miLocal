from fastapi import APIRouter

from api.routes import user, product, store

api_router = APIRouter()
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(product.router, prefix="/product", tags=["product"])
api_router.include_router(store.router, prefix="/store", tags=["store"])
