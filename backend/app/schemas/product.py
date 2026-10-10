from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from app.schemas.category import Category
from app.schemas.sustainability_evidence import SustainabilityEvidence

class ProductBase(BaseModel):
    name: str
    brand: Optional[str] = None
    description: Optional[str] = None
    price: float = Field(..., ge=0)
    currency: str
    image_url: Optional[str] = None
    durability_score: Optional[int] = Field(None, ge=0, le=100)
    packaging_score: Optional[int] = Field(None, ge=0, le=100)
    repairability_score: Optional[int] = Field(None, ge=0, le=100)

class Product(ProductBase):
    id: int
    category_id: int
    created_at: datetime
    updated_at: datetime
    
    overall_sustainability_score: Optional[float] = None
    evidence_coverage: float = 0.0

    model_config = ConfigDict(from_attributes=True)

class ProductDetail(Product):
    category: Category
    evidence: List[SustainabilityEvidence] = []

class PaginatedProducts(BaseModel):
    items: List[Product]
    total: int
    page: int
    page_size: int
    total_pages: int
