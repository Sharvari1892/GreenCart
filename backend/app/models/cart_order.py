"""
Cart and Order models — stored in the same SQLite in-memory database.
Data resets when the backend restarts (demo behaviour, documented).
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True, nullable=False)  # guest cart key
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    added_at = Column(DateTime(timezone=True), server_default=func.now())

    product = relationship("Product")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    status = Column(String, default="confirmed", nullable=False)
    total_amount = Column(Float, nullable=False)
    currency = Column(String, default="INR")
    shipping_name = Column(String, nullable=True)
    shipping_email = Column(String, nullable=True)
    shipping_address = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    product_name = Column(String, nullable=False)
    product_brand = Column(String, nullable=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    currency = Column(String, default="INR")

    order = relationship("Order", back_populates="items")
    product = relationship("Product")
