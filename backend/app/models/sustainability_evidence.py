from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class SustainabilityEvidence(Base):
    __tablename__ = "sustainability_evidence"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    criterion = Column(String, nullable=False) # e.g. durability, packaging, repairability
    source_url = Column(String)
    description = Column(String)
    verification_status = Column(String, default="pending") # pending, verified, rejected
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    product = relationship("Product", back_populates="evidence")
