from typing import List, Optional, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc, asc

from app.models.category import Category
from app.models.product import Product
from app.models.sustainability_evidence import SustainabilityEvidence
from app.services.scoring_service import calculate_evidence_coverage, calculate_overall_score
from app.schemas.product import Product as ProductSchema, ProductDetail, PaginatedProducts

def get_categories(db: Session) -> List[Category]:
    return db.query(Category).all()

def populate_product_scores(product: Product) -> ProductSchema:
    evidence_list = product.evidence
    evidence_coverage = calculate_evidence_coverage(evidence_list)
    overall_score = calculate_overall_score(
        product.durability_score,
        product.packaging_score,
        product.repairability_score,
        evidence_coverage
    )
    
    # Create Pydantic model
    prod_dict = {
        "id": product.id,
        "name": product.name,
        "brand": product.brand,
        "description": product.description,
        "price": product.price,
        "currency": product.currency,
        "image_url": product.image_url,
        "durability_score": product.durability_score,
        "packaging_score": product.packaging_score,
        "repairability_score": product.repairability_score,
        "category_id": product.category_id,
        "created_at": product.created_at,
        "updated_at": product.updated_at,
        "overall_sustainability_score": overall_score,
        "evidence_coverage": evidence_coverage
    }
    return ProductSchema(**prod_dict)

def get_products(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_durability: Optional[int] = None,
    min_packaging: Optional[int] = None,
    min_repairability: Optional[int] = None,
    sort_by: Optional[str] = None,
    sort_desc: bool = False
) -> PaginatedProducts:
    query = db.query(Product)
    
    if search:
        search_filter = f"%{search}%"
        query = query.filter(or_(Product.name.ilike(search_filter), Product.brand.ilike(search_filter)))
    
    if category_id:
        query = query.filter(Product.category_id == category_id)
        
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
        
    if min_durability is not None:
        query = query.filter(Product.durability_score >= min_durability)
    if min_packaging is not None:
        query = query.filter(Product.packaging_score >= min_packaging)
    if min_repairability is not None:
        query = query.filter(Product.repairability_score >= min_repairability)

    # Sorting
    if sort_by:
        sort_col = getattr(Product, sort_by, None)
        if sort_col is not None:
            if sort_desc:
                query = query.order_by(desc(sort_col))
            else:
                query = query.order_by(asc(sort_col))
    
    # Because overall_sustainability_score is computed in python, sorting by it in DB requires repeating the math logic in SQL or we fetch and sort.
    # The prompt says: "Sort by name, price, durability score, or sustainability score."
    # Let's add sustainability score sort in DB.
    # 0.35 * durability + 0.25 * packaging + 0.25 * repairability + 0.15 * evidence quality
    # Computing evidence quality in SQL is very complex (requires subqueries grouping by product_id).
    # Since this is a phase 2 feature and we shouldn't do crazy SQL, if sort_by == 'sustainability_score', we might have to fetch all or approximate. 
    # Let's try to approximate or use a subquery if needed. Actually, let's just fetch and sort if requested, OR sort in DB if we can.
    # Wait, the prompt says: "Use database queries rather than loading the entire catalogue into Python."
    # So I must sort in DB. But `evidence quality` is dynamic.
    # Let's write the SQL expression for the score if possible, or just ignore the evidence part for the sorting if it's too hard? No, that's wrong.
    # Let's create a subquery for evidence coverage.
    
    # Subquery for evidence coverage
    from sqlalchemy import select, func, distinct, cast, Float
    
    # We will get all products, then apply python-side transformations for the response.
    
    total = query.count()
    total_pages = (total + page_size - 1) // page_size
    offset = (page - 1) * page_size
    
    # If we need to sort by sustainability_score in DB:
    if sort_by == "sustainability_score":
        ev_sq = (
            db.query(
                SustainabilityEvidence.product_id,
                (func.count(distinct(SustainabilityEvidence.criterion)) / 3.0 * 100.0).label("ev_cov")
            )
            .filter(
                SustainabilityEvidence.verification_status == "verified",
                SustainabilityEvidence.criterion.in_(["durability", "packaging", "repairability"])
            )
            .group_by(SustainabilityEvidence.product_id)
            .subquery()
        )
        
        # Join with subquery
        query = query.outerjoin(ev_sq, Product.id == ev_sq.c.product_id)
        
        # Calculate score: 0.35 * dur + 0.25 * pack + 0.25 * rep + 0.15 * ev_cov
        # If any is NULL, score is NULL
        from sqlalchemy import case
        score_expr = case(
            (
                and_(
                    Product.durability_score.isnot(None),
                    Product.packaging_score.isnot(None),
                    Product.repairability_score.isnot(None)
                ),
                0.35 * Product.durability_score + 
                0.25 * Product.packaging_score + 
                0.25 * Product.repairability_score + 
                0.15 * func.coalesce(ev_sq.c.ev_cov, 0.0)
            ),
            else_=None
        )
        
        if sort_desc:
            query = query.order_by(desc(score_expr))
        else:
            query = query.order_by(asc(score_expr))

    products = query.offset(offset).limit(page_size).all()
    
    items = [populate_product_scores(p) for p in products]
    
    return PaginatedProducts(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )

def get_product_by_id(db: Session, product_id: int) -> Optional[ProductDetail]:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None
        
    base_prod = populate_product_scores(product)
    
    detail_dict = base_prod.model_dump()
    detail_dict["category"] = product.category
    detail_dict["evidence"] = product.evidence
    
    return ProductDetail(**detail_dict)
