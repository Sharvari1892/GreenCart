from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.category import Category
from app.repositories import product_repo

router = APIRouter()

@router.get("", response_model=List[Category])
def read_categories(db: Session = Depends(get_db)):
    return product_repo.get_categories(db)
