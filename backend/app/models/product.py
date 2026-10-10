from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func, CheckConstraint
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name = Column(String, index=True, nullable=False)
    brand = Column(String)
    description = Column(String)
    price = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    image_url = Column(String)
    
    durability_score = Column(Integer, CheckConstraint('durability_score >= 0 AND durability_score <= 100'), nullable=True)
    packaging_score = Column(Integer, CheckConstraint('packaging_score >= 0 AND packaging_score <= 100'), nullable=True)
    repairability_score = Column(Integer, CheckConstraint('repairability_score >= 0 AND repairability_score <= 100'), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint('price >= 0', name='check_price_positive'),
    )

    category = relationship("Category", back_populates="products")
    evidence = relationship("SustainabilityEvidence", back_populates="product", cascade="all, delete-orphan")
    wishlist_entries = relationship("Wishlist", back_populates="product", cascade="all, delete-orphan")
