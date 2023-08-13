from database.db import db
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field


class Store(db):
    __tablename__ = "stores"
    store_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), index=True)
    status = Column(String(20), default="open")
    address = Column(String, index=True, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    long = Column(Float)
    lat = Column(Float)
    user = relationship("User", back_populates="stores")


class StoreIn(BaseModel):
    name: str = Field(..., min_length=3)
    address: str = Field(..., min_length=3)


class StoreWithUser(StoreIn):
    user_id: int


class StoreOut(BaseModel):
    name: str
    address: str
    status: str
    store_id: int
    user_id: int
