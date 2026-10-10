from typing import Optional, List, TypeVar, Generic
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class Category(CategoryBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
