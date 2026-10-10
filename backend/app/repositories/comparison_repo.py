from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.comparison import Comparison, ComparisonItem
from app.models.product import Product
from app.repositories.product_repo import populate_product_scores
from app.schemas.comparison import ComparisonResponse, ComparisonItemResponse

def create_comparison(db: Session, user_id: int, product_ids: List[int]) -> ComparisonResponse:
    # Verify products exist
    products = db.query(Product).filter(Product.id.in_(product_ids)).all()
    found_ids = {p.id for p in products}
    
    if len(found_ids) != len(product_ids):
        raise ValueError("One or more products not found")
        
    if len(set(product_ids)) != len(product_ids):
        raise ValueError("Duplicate product IDs provided")
        
    if not (2 <= len(product_ids) <= 4):
        raise ValueError("Must compare between 2 and 4 products")
        
    # Create comparison
    comparison = Comparison(user_id=user_id)
    db.add(comparison)
    db.commit()
    db.refresh(comparison)
    
    # Create items
    items = []
    for pid in product_ids:
        item = ComparisonItem(comparison_id=comparison.id, product_id=pid)
        db.add(item)
        items.append(item)
        
    db.commit()
    db.refresh(comparison)
    
    return get_comparison(db, comparison.id)

def get_comparison(db: Session, comparison_id: int) -> Optional[ComparisonResponse]:
    comparison = db.query(Comparison).filter(Comparison.id == comparison_id).first()
    if not comparison:
        return None
        
    items_resp = []
    for item in comparison.items:
        prod_schema = populate_product_scores(item.product)
        items_resp.append(ComparisonItemResponse(product=prod_schema))
        
    return ComparisonResponse(
        id=comparison.id,
        user_id=comparison.user_id,
        created_at=comparison.created_at,
        items=items_resp
    )
