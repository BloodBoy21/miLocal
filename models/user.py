from database.db import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from models.store import Store
from typing import Optional
import re


class User(db):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(20))
    last_name = Column(String(20))
    email = Column(String, unique=True, index=True)
    password = Column(String())
    profile_picture = Column(String, default="")
    stores = relationship(Store, back_populates="user")


class UserIn(BaseModel):
    password: str = Field(
        ...,
        min_length=8,
    )
    email: str = Field(
        ..., pattern=r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+$"
    )
    first_name: str = Field(..., min_length=3, pattern=r"^[a-zA-Z]+$")
    last_name: Optional[str] = Field(min_length=3, pattern=r"^[a-zA-Z]+$", default="")

    @validator("password")
    def validate_password(cls, value):
        password_pattern = (
            "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        )
        if not re.match(password_pattern, value):
            raise ValueError("Password not match with pattern")
        return value


class UserOut(BaseModel):
    first_name: str
    last_name: str
    email: str
    profile_picture: str = None
    user_id: int


class UserLogin(BaseModel):
    email: str
    password: str


class UserLocation(BaseModel):
    lat: float
    lon: float
