from database.db import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from models.store import Store


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
        ..., min_length=8, regex=r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$"
    )
    email: str = Field(..., regex=r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+$")
    first_name: str = Field(..., min_length=3, regex=r"^[a-zA-Z]+$")
    last_name: str = Field(..., min_length=3, regex=r"^[a-zA-Z]+$")


class UserOut(BaseModel):
    first_name: str
    last_name: str
    email: str
    profile_picture: str = None
    user_id: int


class UserLogin(BaseModel):
    email: str
    password: str
