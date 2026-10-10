from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.comparison import ComparisonCreate, ComparisonResponse
from app.repositories import comparison_repo

router = APIRouter()

@router.post("", response_model=ComparisonResponse)
def create_comparison(
    comparison_in: ComparisonCreate,
    db: Session = Depends(get_db)
):
    try:
        # Mocking user_id=1 for now as per rules "require an authenticated user once Phase 3 authentication is available"
        user_id = 1 
        return comparison_repo.create_comparison(db, user_id=user_id, product_ids=comparison_in.product_ids)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{comparison_id}", response_model=ComparisonResponse)
def read_comparison(comparison_id: int, db: Session = Depends(get_db)):
    comparison = comparison_repo.get_comparison(db, comparison_id)
    if not comparison:
        raise HTTPException(status_code=404, detail="Comparison not found")
    return comparison
