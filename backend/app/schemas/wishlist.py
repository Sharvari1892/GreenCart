from typing import List
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.schemas.product import Product

class WishlistCreate(BaseModel):
    product_id: int

class WishlistResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    created_at: datetime
    product: Product

    model_config = ConfigDict(from_attributes=True)
