from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db, get_current_user
from app.schemas.wishlist import WishlistCreate, WishlistResponse
from app.models.wishlist import Wishlist
from app.models.product import Product
from app.models.user import User
from app.repositories import product_repo

router = APIRouter()

@router.post("", response_model=WishlistResponse)
def add_to_wishlist(
    item_in: WishlistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == item_in.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    existing = db.query(Wishlist).filter(
        Wishlist.user_id == current_user.id,
        Wishlist.product_id == item_in.product_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Product already in wishlist")
        
    new_item = Wishlist(user_id=current_user.id, product_id=item_in.product_id)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    
    return {
        "id": new_item.id,
        "user_id": new_item.user_id,
        "product_id": new_item.product_id,
        "created_at": new_item.created_at,
        "product": product_repo.populate_product_scores(new_item.product)
    }

@router.get("", response_model=List[WishlistResponse])
def get_wishlists(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 20
):
    items = db.query(Wishlist).filter(Wishlist.user_id == current_user.id).offset(skip).limit(limit).all()
    
    res = []
    for item in items:
        item_dict = {
            "id": item.id,
            "user_id": item.user_id,
            "product_id": item.product_id,
            "created_at": item.created_at,
            "product": product_repo.populate_product_scores(item.product)
        }
        res.append(item_dict)
        
    return res

@router.delete("/{product_id}")
def remove_from_wishlist(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = db.query(Wishlist).filter(
        Wishlist.user_id == current_user.id,
        Wishlist.product_id == product_id
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Product not in wishlist")
        
    db.delete(item)
    db.commit()
    return {"msg": "Removed from wishlist"}
