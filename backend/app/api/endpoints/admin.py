from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_admin_user
from app.models.product import Product
from app.models.sustainability_evidence import SustainabilityEvidence
from app.models.user import User
from app.schemas.admin import ProductCreate, ProductUpdate, EvidenceCreate, EvidenceUpdate, EvidenceVerificationUpdate
from app.schemas.product import ProductDetail
from app.schemas.sustainability_evidence import SustainabilityEvidence as EvidenceSchema
from app.repositories import product_repo

router = APIRouter()

@router.post("/products", response_model=ProductDetail)
def create_product(
    prod_in: ProductCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    new_prod = Product(**prod_in.model_dump())
    db.add(new_prod)
    db.commit()
    db.refresh(new_prod)
    return product_repo.get_product_by_id(db, new_prod.id)

@router.patch("/products/{product_id}", response_model=ProductDetail)
def update_product(
    product_id: int,
    prod_in: ProductUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    prod = db.query(Product).filter(Product.id == product_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
        
    update_data = prod_in.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(prod, k, v)
        
    db.commit()
    db.refresh(prod)
    return product_repo.get_product_by_id(db, prod.id)

@router.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    prod = db.query(Product).filter(Product.id == product_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
        
    # Handled by cascade="all, delete-orphan" for evidence, wishlist, comparison_items
    # But let's be explicit and safe. Wishlist and comparison items have delete-orphan set.
    db.delete(prod)
    db.commit()
    return {"msg": "Product deleted successfully"}

@router.post("/evidence", response_model=EvidenceSchema)
def create_evidence(
    ev_in: EvidenceCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    prod = db.query(Product).filter(Product.id == ev_in.product_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
        
    new_ev = SustainabilityEvidence(**ev_in.model_dump(), verification_status="pending")
    db.add(new_ev)
    db.commit()
    db.refresh(new_ev)
    return new_ev

@router.patch("/evidence/{evidence_id}", response_model=EvidenceSchema)
def update_evidence(
    evidence_id: int,
    ev_in: EvidenceUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    ev = db.query(SustainabilityEvidence).filter(SustainabilityEvidence.id == evidence_id).first()
    if not ev:
        raise HTTPException(status_code=404, detail="Evidence not found")
        
    update_data = ev_in.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(ev, k, v)
        
    db.commit()
    db.refresh(ev)
    return ev

@router.patch("/evidence/{evidence_id}/verification", response_model=EvidenceSchema)
def verify_evidence(
    evidence_id: int,
    ver_in: EvidenceVerificationUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    ev = db.query(SustainabilityEvidence).filter(SustainabilityEvidence.id == evidence_id).first()
    if not ev:
        raise HTTPException(status_code=404, detail="Evidence not found")
        
    ev.verification_status = ver_in.verification_status
    db.commit()
    db.refresh(ev)
    return ev
