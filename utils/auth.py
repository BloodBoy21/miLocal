import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
import os
from repositories.user_repository import UserRepository
from models.user import User

user_repository = UserRepository()
JWT_SECRET = os.getenv("JWT_SECRET")


async def auth_user(auth: str = Depends(HTTPBearer())) -> User:
    try:
        payload = jwt.decode(auth.credentials, JWT_SECRET, algorithms=["HS256"])
        return user_repository.find_by_id(payload.get("user_id"))
    except jwt.exceptions.InvalidSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired token",
        )
    except jwt.exceptions.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
