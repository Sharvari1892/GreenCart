import pytest
from app.models.category import Category
from app.models.product import Product
from app.models.product_replacement import ProductReplacement
from app.models.sustainability_evidence import SustainabilityEvidence

def test_product_fields_and_replacements(db, client):
    # Create category
    cat = Category(name="Test Personal Care", description="Care items")
    db.add(cat)
    db.commit()

    # Create conventional product
    p_conv = Product(
        name="Plastic Toothbrush Test",
        brand="Brand X",
        price=30.0,
        currency="INR",
        materials="Polypropylene",
        purchase_url="https://example.com/conv",
        is_sustainable=False,
        category_id=cat.id,
        durability_score=30,
        packaging_score=20,
        repairability_score=0
    )
    # Create sustainable replacement product
    p_sust = Product(
        name="Bamboo Toothbrush Test",
        brand="Brand Eco",
        price=50.0,
        currency="INR",
        materials="Bamboo, nylon bristles",
        purchase_url="https://example.com/sust",
        is_sustainable=True,
        category_id=cat.id,
        durability_score=75,
        packaging_score=90,
        repairability_score=10
    )
    db.add_all([p_conv, p_sust])
    db.commit()

    # Create replacement relationship
    rel = ProductReplacement(
        original_product_id=p_conv.id,
        replacement_product_id=p_sust.id,
        replacement_type="composition_change",
        reason="Bamboo replaces virgin plastic handle.",
        main_change="Handle material changed from polypropylene to natural bamboo.",
        known_limitations="Nylon bristles must still be plucked before composting."
    )
    db.add(rel)
    db.commit()

    # Add verified evidence
    ev = SustainabilityEvidence(
        product_id=p_sust.id,
        criterion="packaging",
        source_url="https://example.com/packaging-cert",
        description="100% plastic-free recycled paper carton.",
        verification_status="verified"
    )
    db.add(ev)
    db.commit()

    # Test GET /api/products
    res = client.get("/api/products?search=Toothbrush Test")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 2
    items = {item["name"]: item for item in data["items"]}
    assert "Plastic Toothbrush Test" in items
    assert "Bamboo Toothbrush Test" in items
    
    # Verify fields
    conv_data = items["Plastic Toothbrush Test"]
    assert conv_data["currency"] == "INR"
    assert conv_data["materials"] == "Polypropylene"
    assert conv_data["is_sustainable"] is False

    sust_data = items["Bamboo Toothbrush Test"]
    assert sust_data["currency"] == "INR"
    assert sust_data["is_sustainable"] is True
    assert sust_data["evidence_coverage"] > 0
    assert "source_verification_status" in sust_data

    # Test GET /api/products/{id} includes replacements
    detail_res = client.get(f"/api/products/{p_conv.id}")
    assert detail_res.status_code == 200
    detail_data = detail_res.json()
    assert len(detail_data["replacements"]) >= 1
    rep_item = detail_data["replacements"][0]
    assert rep_item["replacement_product_id"] == p_sust.id
    assert rep_item["replacement_type"] == "composition_change"
    assert rep_item["known_limitations"] == "Nylon bristles must still be plucked before composting."


def test_database_configuration_guards():
    from app.core.config import Settings
    import os

    # 1. Verify default database is PostgreSQL
    s_default = Settings(ENVIRONMENT="development")
    assert s_default.SQLALCHEMY_DATABASE_URI.startswith("postgresql")

    # 2. Verify SQLite is prohibited outside test environment
    with pytest.raises(ValueError, match="SQLite is only permitted in isolated test environments"):
        Settings(ENVIRONMENT="development", DATABASE_URL="sqlite:///./unauthorized.db")

    with pytest.raises(ValueError, match="SQLite is only permitted in isolated test environments"):
        Settings(ENVIRONMENT="production", DATABASE_URL="sqlite:///./prod.db")

    # 3. Verify SQLite IS allowed when explicitly ENVIRONMENT="test"
    s_test = Settings(ENVIRONMENT="test", DATABASE_URL="sqlite:///:memory:")
    assert "sqlite" in s_test.SQLALCHEMY_DATABASE_URI


def test_scoring_safety_and_missing_data(db, client):
    from app.services.scoring_service import calculate_overall_score, calculate_evidence_coverage
    
    cat = Category(name="Test Scoring Cat", description="Testing scores")
    db.add(cat)
    db.commit()

    # 1. Product with missing repairability (e.g. single-use consumable)
    p_incomplete = Product(
        name="Single Use Cup Test",
        price=10.0,
        currency="INR",
        is_sustainable=True,
        category_id=cat.id,
        durability_score=20,
        packaging_score=50,
        repairability_score=None, # Missing data must NOT be silently treated as 0 or positive
        source_verification_status="manufacturer_info_only"
    )
    db.add(p_incomplete)
    db.commit()

    score = calculate_overall_score(
        durability=p_incomplete.durability_score,
        packaging=p_incomplete.packaging_score,
        repairability=p_incomplete.repairability_score,
        evidence_coverage=0.0
    )
    # Overall score must be None (not invented)
    assert score is None

    # 2. is_sustainable=True does NOT automatically grant evidence coverage or boost score
    assert calculate_evidence_coverage([]) == 0.0

    # 3. Evidence with 'manufacturer_reported' does NOT count toward verified evidence coverage
    ev_mfg = SustainabilityEvidence(
        product_id=p_incomplete.id,
        criterion="packaging",
        source_url="https://example.com/mfg-claim",
        description="Self-reported packaging claim",
        verification_status="manufacturer_reported"
    )
    db.add(ev_mfg)
    db.commit()

    cov = calculate_evidence_coverage([ev_mfg])
    assert cov == 0.0  # Only 'verified' counts!

    # 4. Verified evidence DOES count toward evidence coverage
    ev_verified = SustainabilityEvidence(
        product_id=p_incomplete.id,
        criterion="packaging",
        source_url="https://example.com/audit",
        description="Audited packaging cert",
        verification_status="verified"
    )
    db.add(ev_verified)
    db.commit()

    cov_verified = calculate_evidence_coverage([ev_mfg, ev_verified])
    assert cov_verified > 0.0
