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
        "currency": product.currency or "INR",
        "image_url": product.image_url,
        "materials": product.materials,
        "purchase_url": product.purchase_url,
        "source_verification_status": product.source_verification_status or "unverified",
        "is_sustainable": product.is_sustainable if product.is_sustainable is not None else False,
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
        query = query.outerjoin(Category, Product.category_id == Category.id).filter(
            or_(
                Product.name.ilike(search_filter),
                Product.brand.ilike(search_filter),
                Product.materials.ilike(search_filter),
                Category.name.ilike(search_filter),
            )
        )
    
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
    
    # Subquery for evidence coverage
    from sqlalchemy import select, func, distinct, cast, Float
    
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
    detail_dict["replacements"] = product.replacements_for
    
    return ProductDetail(**detail_dict)

def get_product_replacements(db: Session, product_id: int) -> Optional[List[dict]]:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None

    from app.models.product_replacement import ProductReplacement
    replacements = (
        db.query(ProductReplacement)
        .filter(ProductReplacement.original_product_id == product_id)
        .all()
    )
    result = []
    for rep in replacements:
        sust_prod = populate_product_scores(rep.replacement_product)
        result.append({
            "id": rep.id,
            "original_product_id": rep.original_product_id,
            "replacement_product_id": rep.replacement_product_id,
            "replacement_type": rep.replacement_type,
            "reason": rep.reason,
            "main_change": rep.main_change,
            "known_limitations": rep.known_limitations,
            "created_at": rep.created_at,
            "replacement_product": sust_prod,
            "price": sust_prod.price,
            "overall_sustainability_score": sust_prod.overall_sustainability_score,
            "evidence_coverage": sust_prod.evidence_coverage,
            "source_verification_status": sust_prod.source_verification_status,
        })
    return result
