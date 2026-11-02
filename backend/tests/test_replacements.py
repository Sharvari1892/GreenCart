import pytest
from app.models.category import Category
from app.models.product import Product
from app.models.product_replacement import ProductReplacement
from app.models.sustainability_evidence import SustainabilityEvidence

def test_replacement_endpoints_and_isolation(db, client):
    # 1. Setup category
    cat = Category(name="Personal Care", description="Everyday personal hygiene")
    db.add(cat)
    db.commit()

    # 2. Setup conventional product
    p_orig = Product(
        name="Plastic Toothbrush Standard",
        brand="OralBrand",
        price=40.0,
        currency="INR",
        materials="Polypropylene plastic handle, nylon bristles",
        purchase_url="https://example.com/oralbrand",
        source_verification_status="manufacturer_info_only",
        is_sustainable=False,
        category_id=cat.id,
        durability_score=25,
        packaging_score=20,
        repairability_score=None
    )
    # 3. Setup replacement product
    p_alt = Product(
        name="Bamboo Toothbrush Eco",
        brand="EcoBrand",
        price=120.0,
        currency="INR",
        materials="Moso bamboo handle, charcoal nylon bristles",
        purchase_url="https://example.com/ecobrand",
        source_verification_status="verified_exact_source",
        is_sustainable=True,
        category_id=cat.id,
        durability_score=80,
        packaging_score=95,
        repairability_score=20
    )
    # 4. Setup unrelated product (should NOT be returned in replacements)
    p_unrelated = Product(
        name="Stainless Steel Straw",
        brand="GreenSip",
        price=200.0,
        currency="INR",
        materials="Food-grade 304 stainless steel",
        purchase_url="https://example.com/straw",
        source_verification_status="verified_exact_source",
        is_sustainable=True,
        category_id=cat.id,
        durability_score=95,
        packaging_score=90,
        repairability_score=90
    )
    db.add_all([p_orig, p_alt, p_unrelated])
    db.commit()

    # Add verified evidence to replacement product
    ev1 = SustainabilityEvidence(
        product_id=p_alt.id,
        criterion="packaging",
        source_url="https://example.com/pack-cert",
        description="FSC certified 100% compostable unbleached kraft box",
        verification_status="verified"
    )
    db.add(ev1)
    db.commit()

    # Create replacement relationship
    rel = ProductReplacement(
        original_product_id=p_orig.id,
        replacement_product_id=p_alt.id,
        replacement_type="composition_change",
        reason="Replaces petroleum polypropylene with rapidly renewable compostable Moso bamboo.",
        main_change="Plastic handle upgraded to 100% natural organic bamboo.",
        known_limitations="Bristles still contain charcoal-infused nylon and must be separated."
    )
    db.add(rel)
    db.commit()

    # ── Test 1: GET /api/products/{id}/replacements returns replacements with correct fields ──
    res = client.get(f"/api/products/{p_orig.id}/replacements")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) == 1

    item = data[0]
    assert item["id"] == rel.id
    assert item["original_product_id"] == p_orig.id
    assert item["replacement_product_id"] == p_alt.id
    assert item["replacement_type"] == "composition_change"
    assert item["reason"] == "Replaces petroleum polypropylene with rapidly renewable compostable Moso bamboo."
    assert item["main_change"] == "Plastic handle upgraded to 100% natural organic bamboo."
    assert item["known_limitations"] == "Bristles still contain charcoal-infused nylon and must be separated."

    # Replacement product details
    rep_prod = item["replacement_product"]
    assert rep_prod["id"] == p_alt.id
    assert rep_prod["name"] == "Bamboo Toothbrush Eco"
    assert rep_prod["price"] == 120.0
    assert rep_prod["currency"] == "INR"
    assert rep_prod["source_verification_status"] == "verified_exact_source"
    assert rep_prod["overall_sustainability_score"] is not None
    assert rep_prod["evidence_coverage"] > 0

    # Direct top-level convenience fields
    assert item["price"] == 120.0
    assert item["source_verification_status"] == "verified_exact_source"
    assert item["evidence_coverage"] > 0

    # ── Test 2: Unrelated product is NOT returned ──
    assert item["replacement_product_id"] != p_unrelated.id

    # ── Test 3: Product with no replacements returns empty array ──
    res_empty = client.get(f"/api/products/{p_unrelated.id}/replacements")
    assert res_empty.status_code == 200
    assert res_empty.json() == []

    # ── Test 4: Invalid product ID returns 404 ──
    res_404 = client.get("/api/products/999999/replacements")
    assert res_404.status_code == 404
    assert res_404.json()["detail"] == "Product not found"


def test_product_search_by_material_and_category(db, client):
    cat_kitchen = Category(name="Kitchen & Dining", description="Kitchen items")
    db.add(cat_kitchen)
    db.commit()

    p_glass = Product(
        name="Aero Container",
        brand="GlassCo",
        price=350.0,
        currency="INR",
        materials="Pure Borosilicate Glass",
        purchase_url="https://example.com/glass",
        source_verification_status="verified_exact_source",
        is_sustainable=True,
        category_id=cat_kitchen.id,
        durability_score=90,
        packaging_score=85,
        repairability_score=70
    )
    db.add(p_glass)
    db.commit()

    # Search by material "Borosilicate"
    res_mat = client.get("/api/products?search=Borosilicate")
    assert res_mat.status_code == 200
    items_mat = res_mat.json()["items"]
    assert any(p["name"] == "Aero Container" for p in items_mat)

    # Search by category name "Kitchen & Dining"
    res_cat = client.get("/api/products?search=Kitchen")
    assert res_cat.status_code == 200
    items_cat = res_cat.json()["items"]
    assert any(p["name"] == "Aero Container" for p in items_cat)
