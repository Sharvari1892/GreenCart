from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, func, CheckConstraint
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    brand = Column(String, index=True)
    description = Column(String)
    price = Column(Float, index=True, nullable=False)
    currency = Column(String, default="INR")
    image_url = Column(String)
    materials = Column(String, nullable=True)
    purchase_url = Column(String, nullable=True)
    source_verification_status = Column(String, default="unverified", nullable=False)
    is_sustainable = Column(Boolean, default=False, nullable=False)
    
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
    replacements_for = relationship(
        "ProductReplacement",
        foreign_keys="ProductReplacement.original_product_id",
        back_populates="original_product",
        cascade="all, delete-orphan"
    )
    replacements_by = relationship(
        "ProductReplacement",
        foreign_keys="ProductReplacement.replacement_product_id",
        back_populates="replacement_product",
        cascade="all, delete-orphan"
    )
