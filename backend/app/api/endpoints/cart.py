"""
Cart API — session-based guest cart stored in SQLite in-memory.
Cart data resets when the backend restarts (demo behaviour).
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.api.deps import get_db
from app.models.cart_order import CartItem
from app.models.product import Product
import uuid

router = APIRouter()


# ── Schemas ───────────────────────────────────────────────────────────────────

class CartItemAdd(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemUpdate(BaseModel):
    quantity: int


class CartItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    product_name: str
    product_brand: Optional[str]
    product_price: float
    product_image: Optional[str]
    currency: str
    subtotal: float

    class Config:
        from_attributes = True


class CartOut(BaseModel):
    session_id: str
    items: List[CartItemOut]
    total: float
    item_count: int


# ── Helpers ───────────────────────────────────────────────────────────────────

def get_or_create_session(x_session_id: Optional[str] = Header(None)) -> str:
    return x_session_id or str(uuid.uuid4())


def build_cart_out(session_id: str, items: list, db: Session) -> CartOut:
    result = []
    total = 0.0
    for item in items:
        p: Product = item.product
        subtotal = p.price * item.quantity
        total += subtotal
        result.append(CartItemOut(
            id=item.id,
            product_id=item.product_id,
            quantity=item.quantity,
            product_name=p.name,
            product_brand=p.brand,
            product_price=p.price,
            product_image=p.image_url,
            currency=p.currency or "INR",
            subtotal=subtotal,
        ))
    return CartOut(
        session_id=session_id,
        items=result,
        total=round(total, 2),
        item_count=sum(i.quantity for i in items),
    )


# ── Routes ────────────────────────────────────────────────────────────────────

@router.get("", response_model=CartOut)
def get_cart(
    db: Session = Depends(get_db),
    x_session_id: Optional[str] = Header(None),
):
    session_id = x_session_id or ""
    if not session_id:
        return CartOut(session_id="", items=[], total=0.0, item_count=0)
    items = db.query(CartItem).filter(CartItem.session_id == session_id).all()
    return build_cart_out(session_id, items, db)


@router.post("", response_model=CartOut)
def add_to_cart(
    body: CartItemAdd,
    db: Session = Depends(get_db),
    x_session_id: Optional[str] = Header(None),
):
    session_id = get_or_create_session(x_session_id)
    product = db.query(Product).filter(Product.id == body.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    existing = db.query(CartItem).filter(
        CartItem.session_id == session_id,
        CartItem.product_id == body.product_id,
    ).first()

    if existing:
        existing.quantity += body.quantity
    else:
        db.add(CartItem(
            session_id=session_id,
            product_id=body.product_id,
            quantity=body.quantity,
        ))
    db.commit()

    items = db.query(CartItem).filter(CartItem.session_id == session_id).all()
    return build_cart_out(session_id, items, db)


@router.put("/{item_id}", response_model=CartOut)
def update_cart_item(
    item_id: int,
    body: CartItemUpdate,
    db: Session = Depends(get_db),
    x_session_id: Optional[str] = Header(None),
):
    session_id = x_session_id or ""
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.session_id == session_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    if body.quantity <= 0:
        db.delete(item)
    else:
        item.quantity = body.quantity
    db.commit()
    items = db.query(CartItem).filter(CartItem.session_id == session_id).all()
    return build_cart_out(session_id, items, db)


@router.delete("/{item_id}", response_model=CartOut)
def remove_cart_item(
    item_id: int,
    db: Session = Depends(get_db),
    x_session_id: Optional[str] = Header(None),
):
    session_id = x_session_id or ""
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.session_id == session_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(item)
    db.commit()
    items = db.query(CartItem).filter(CartItem.session_id == session_id).all()
    return build_cart_out(session_id, items, db)


@router.delete("", response_model=CartOut)
def clear_cart(
    db: Session = Depends(get_db),
    x_session_id: Optional[str] = Header(None),
):
    session_id = x_session_id or ""
    db.query(CartItem).filter(CartItem.session_id == session_id).delete()
    db.commit()
    return CartOut(session_id=session_id, items=[], total=0.0, item_count=0)
