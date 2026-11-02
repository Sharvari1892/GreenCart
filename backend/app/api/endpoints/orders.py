"""
Orders API — mock checkout that stores orders in SQLite in-memory.
Order data resets when the backend restarts (demo behaviour).
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.api.deps import get_db
from app.models.cart_order import CartItem, Order, OrderItem
from app.models.product import Product

router = APIRouter()


# ── Schemas ───────────────────────────────────────────────────────────────────

class CheckoutRequest(BaseModel):
    shipping_name: str
    shipping_email: str
    shipping_address: str
    payment_method: str = "demo_cod"  # demo only


class OrderItemOut(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_brand: Optional[str]
    quantity: int
    unit_price: float
    currency: str
    subtotal: float

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: int
    status: str
    total_amount: float
    currency: str
    shipping_name: str
    shipping_email: str
    shipping_address: str
    items: List[OrderItemOut]
    created_at: str

    class Config:
        from_attributes = True


# ── Routes ────────────────────────────────────────────────────────────────────

@router.post("", response_model=OrderOut)
def checkout(
    body: CheckoutRequest,
    db: Session = Depends(get_db),
    x_session_id: Optional[str] = Header(None),
):
    session_id = x_session_id or ""
    cart_items = db.query(CartItem).filter(CartItem.session_id == session_id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = 0.0
    order_items = []
    for item in cart_items:
        p: Product = item.product
        subtotal = p.price * item.quantity
        total += subtotal
        order_items.append({
            "product_id": p.id,
            "product_name": p.name,
            "product_brand": p.brand,
            "quantity": item.quantity,
            "unit_price": p.price,
            "currency": p.currency or "INR",
        })

    order = Order(
        session_id=session_id,
        status="confirmed",
        total_amount=round(total, 2),
        currency="INR",
        shipping_name=body.shipping_name,
        shipping_email=body.shipping_email,
        shipping_address=body.shipping_address,
    )
    db.add(order)
    db.flush()

    for oi in order_items:
        db.add(OrderItem(order_id=order.id, **oi))

    # Clear cart after checkout
    db.query(CartItem).filter(CartItem.session_id == session_id).delete()
    db.commit()
    db.refresh(order)

    return _order_out(order)


@router.get("", response_model=List[OrderOut])
def list_orders(
    db: Session = Depends(get_db),
    x_session_id: Optional[str] = Header(None),
):
    session_id = x_session_id or ""
    orders = db.query(Order).filter(Order.session_id == session_id).order_by(Order.id.desc()).all()
    return [_order_out(o) for o in orders]


@router.get("/{order_id}", response_model=OrderOut)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    x_session_id: Optional[str] = Header(None),
):
    session_id = x_session_id or ""
    order = db.query(Order).filter(Order.id == order_id, Order.session_id == session_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return _order_out(order)


def _order_out(order: Order) -> OrderOut:
    items = []
    for oi in order.items:
        items.append(OrderItemOut(
            id=oi.id,
            product_id=oi.product_id,
            product_name=oi.product_name,
            product_brand=oi.product_brand,
            quantity=oi.quantity,
            unit_price=oi.unit_price,
            currency=oi.currency,
            subtotal=round(oi.unit_price * oi.quantity, 2),
        ))
    return OrderOut(
        id=order.id,
        status=order.status,
        total_amount=order.total_amount,
        currency=order.currency,
        shipping_name=order.shipping_name,
        shipping_email=order.shipping_email,
        shipping_address=order.shipping_address,
        items=items,
        created_at=str(order.created_at),
    )
