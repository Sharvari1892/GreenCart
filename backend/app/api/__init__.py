from fastapi import APIRouter
from app.api.endpoints import (
    health,
    categories,
    products,
    comparisons,
    auth,
    wishlists,
    admin,
    cart,
    orders,
    external_compare,
)

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(comparisons.router, prefix="/comparisons", tags=["comparisons"])
api_router.include_router(wishlists.router, prefix="/wishlists", tags=["wishlists"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(cart.router, prefix="/cart", tags=["cart"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(external_compare.router, prefix="/external-compare", tags=["external-compare"])
