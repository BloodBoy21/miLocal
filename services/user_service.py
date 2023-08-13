from models.user import UserIn, UserOut, UserLogin
from repositories.user_repository import UserRepository
from fastapi import HTTPException, status
from utils.security import get_password_hash, generate_token, check_password_hash

user_repository = UserRepository()


def create_user(user: UserIn) -> dict:
    if user_repository.exists(user.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )
    user.password = get_password_hash(user.password)
    new_user = user_repository.create(user)
    user_out = UserOut(**new_user.__dict__)
    token = generate_token(user_out.user_id)
    return {"token": token, "user": user_out}


def login_user(user: UserLogin) -> dict:
    user_db = user_repository.get_by_email(user.email)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    if not check_password_hash(user.password, user_db.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    user_out = UserOut(**user_db.__dict__)
    token = generate_token(user_out.user_id)
    return {"token": token}
