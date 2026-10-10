from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Comparison(Base):
    __tablename__ = "comparisons"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="comparisons")
    items = relationship("ComparisonItem", back_populates="comparison", cascade="all, delete-orphan")

class ComparisonItem(Base):
    __tablename__ = "comparison_items"

    comparison_id = Column(Integer, ForeignKey("comparisons.id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    comparison = relationship("Comparison", back_populates="items")
    product = relationship("Product")
