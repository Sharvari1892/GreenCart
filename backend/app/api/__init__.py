from fastapi import APIRouter
from app.api.endpoints import health, categories, products, comparisons

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(comparisons.router, prefix="/comparisons", tags=["comparisons"])
