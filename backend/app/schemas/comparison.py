from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.schemas.product import Product

class ComparisonCreate(BaseModel):
    product_ids: List[int]

class ComparisonItemResponse(BaseModel):
    product: Product

    model_config = ConfigDict(from_attributes=True)

class ComparisonResponse(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    items: List[ComparisonItemResponse]

    model_config = ConfigDict(from_attributes=True)
