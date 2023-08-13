from database.db import db
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field


class ProductReport(db):
    __tablename__ = "product_reports"
    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    sku = Column(String, index=True)
    count = Column(Integer)
    created_at = Column(DateTime)
