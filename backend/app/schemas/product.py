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
    currency: str = "INR"
    image_url: Optional[str] = None
    materials: Optional[str] = None
    purchase_url: Optional[str] = None
    source_verification_status: str = "unverified"
    is_sustainable: bool = False
    durability_score: Optional[int] = Field(None, ge=0, le=100)
    packaging_score: Optional[int] = Field(None, ge=0, le=100)
    repairability_score: Optional[int] = Field(None, ge=0, le=100)

class ProductReplacementDetail(BaseModel):
    id: int
    original_product_id: int
    replacement_product_id: int
    replacement_type: str
    reason: str
    main_change: str
    known_limitations: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class Product(ProductBase):
    id: int
    category_id: int
    created_at: datetime
    updated_at: datetime
    
    overall_sustainability_score: Optional[float] = None
    evidence_coverage: float = 0.0

    model_config = ConfigDict(from_attributes=True)

class ReplacementWithProduct(BaseModel):
    id: int
    original_product_id: int
    replacement_product_id: int
    replacement_type: str
    reason: str
    main_change: str
    known_limitations: Optional[str] = None
    created_at: datetime
    replacement_product: Product
    price: Optional[float] = None
    overall_sustainability_score: Optional[float] = None
    evidence_coverage: float = 0.0
    source_verification_status: str = "unverified"

    model_config = ConfigDict(from_attributes=True)

class ProductDetail(Product):
    category: Category
    evidence: List[SustainabilityEvidence] = []
    replacements: List[ProductReplacementDetail] = []

class PaginatedProducts(BaseModel):
    items: List[Product]
    total: int
    page: int
    page_size: int
    total_pages: int
