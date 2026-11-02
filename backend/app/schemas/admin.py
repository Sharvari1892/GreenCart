from typing import Optional
from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    category_id: int
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

class ProductUpdate(BaseModel):
    category_id: Optional[int] = None
    name: Optional[str] = None
    brand: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    currency: Optional[str] = None
    image_url: Optional[str] = None
    materials: Optional[str] = None
    purchase_url: Optional[str] = None
    source_verification_status: Optional[str] = None
    is_sustainable: Optional[bool] = None
    durability_score: Optional[int] = Field(None, ge=0, le=100)
    packaging_score: Optional[int] = Field(None, ge=0, le=100)
    repairability_score: Optional[int] = Field(None, ge=0, le=100)

class EvidenceCreate(BaseModel):
    product_id: int
    criterion: str = Field(..., pattern="^(durability|packaging|repairability)$")
    source_url: Optional[str] = None
    description: Optional[str] = None

class EvidenceUpdate(BaseModel):
    criterion: Optional[str] = Field(None, pattern="^(durability|packaging|repairability)$")
    source_url: Optional[str] = None
    description: Optional[str] = None

class EvidenceVerificationUpdate(BaseModel):
    verification_status: str = Field(..., pattern="^(pending|verified|rejected)$")
