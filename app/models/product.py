from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON

from app.db.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # Store first 3 sponsored products as JSON
    sponsored_products = Column(JSON, nullable=True)

    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(String, unique=True, nullable=False, index=True)

    title = Column(String, nullable=True)
    description = Column(String, nullable=True)

    # List of image URLs
    image_urls = Column(JSON, nullable=True)

    rating = Column(Float, nullable=True)
    rating_count = Column(Integer, nullable=True)

    brand = Column(String, nullable=True)

    price = Column(Float, nullable=True)
    currency = Column(String, nullable=True)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    category = relationship("Category", back_populates="products")