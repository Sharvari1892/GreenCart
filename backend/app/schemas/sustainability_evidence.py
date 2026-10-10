from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class SustainabilityEvidenceBase(BaseModel):
    criterion: str
    source_url: Optional[str] = None
    description: Optional[str] = None
    verification_status: str

class SustainabilityEvidence(SustainabilityEvidenceBase):
    id: int
    product_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
