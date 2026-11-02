from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.schemas.comparison import ComparisonCreate, ComparisonResponse
from app.repositories import comparison_repo
from app.models.user import User

router = APIRouter()

@router.post("", response_model=ComparisonResponse)
def create_comparison(
    comparison_in: ComparisonCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return comparison_repo.create_comparison(db, user_id=current_user.id, product_ids=comparison_in.product_ids)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{comparison_id}", response_model=ComparisonResponse)
def read_comparison(
    comparison_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comparison = comparison_repo.get_comparison(db, comparison_id)
    if not comparison:
        raise HTTPException(status_code=404, detail="Comparison not found")
    if comparison.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this comparison")
    return comparison
