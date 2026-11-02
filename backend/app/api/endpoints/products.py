from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.product import ProductDetail, PaginatedProducts, ReplacementWithProduct
from app.schemas.sustainability_evidence import SustainabilityEvidence
from app.repositories import product_repo, evidence_repo

router = APIRouter()

@router.get("", response_model=PaginatedProducts)
def read_products(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    min_durability: Optional[int] = Query(None, ge=0, le=100),
    min_packaging: Optional[int] = Query(None, ge=0, le=100),
    min_repairability: Optional[int] = Query(None, ge=0, le=100),
    sort_by: Optional[str] = Query(None, pattern="^(name|price|durability_score|sustainability_score)$"),
    sort_desc: bool = False
):
    return product_repo.get_products(
        db=db,
        page=page,
        page_size=page_size,
        search=search,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        min_durability=min_durability,
        min_packaging=min_packaging,
        min_repairability=min_repairability,
        sort_by=sort_by,
        sort_desc=sort_desc
    )

@router.get("/{product_id}", response_model=ProductDetail)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = product_repo.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/{product_id}/evidence", response_model=List[SustainabilityEvidence])
def read_product_evidence(product_id: int, db: Session = Depends(get_db)):
    product = product_repo.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return evidence_repo.get_evidence_for_product(db, product_id)

@router.get("/{product_id}/replacements", response_model=List[ReplacementWithProduct])
def read_product_replacements(product_id: int, db: Session = Depends(get_db)):
    replacements = product_repo.get_product_replacements(db, product_id)
    if replacements is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return replacements
