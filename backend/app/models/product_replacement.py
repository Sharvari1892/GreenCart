from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class ProductReplacement(Base):
    __tablename__ = "product_replacements"

    id = Column(Integer, primary_key=True, index=True)
    original_product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    replacement_product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    
    # Types: "composition_change", "design_change", "entire_product_replacement"
    replacement_type = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    main_change = Column(String, nullable=False)
    known_limitations = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    original_product = relationship(
        "Product",
        foreign_keys=[original_product_id],
        back_populates="replacements_for"
    )
    replacement_product = relationship(
        "Product",
        foreign_keys=[replacement_product_id],
        back_populates="replacements_by"
    )
