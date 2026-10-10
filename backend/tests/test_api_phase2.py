import pytest
from app.models.category import Category
from app.models.product import Product
from app.models.user import User

@pytest.fixture(scope="module")
def setup_data(db):
    user = User(name="Test User", email="test2@example.com", password_hash="hash")
    db.add(user)
    cat = Category(name="Test Category")
    db.add(cat)
    db.commit()
    
    p1 = Product(name="Product 1", brand="Brand A", price=10, category_id=cat.id, durability_score=80, packaging_score=80, repairability_score=80)
    p2 = Product(name="Product 2", brand="Brand B", price=20, category_id=cat.id, durability_score=90, packaging_score=90, repairability_score=90)
    p3 = Product(name="Product 3", brand="Brand A", price=30, category_id=cat.id)
    db.add_all([p1, p2, p3])
    db.commit()
    return {"cat": cat, "p1": p1, "p2": p2, "p3": p3}

def test_get_categories(client, setup_data):
    res = client.get("/api/categories")
    assert res.status_code == 200
    assert len(res.json()) >= 1

def test_get_products(client, setup_data):
    res = client.get("/api/products")
    assert res.status_code == 200
    data = res.json()
    assert "items" in data
    assert data["total"] >= 3

def test_get_products_filter(client, setup_data):
    res = client.get("/api/products?min_price=15")
    assert res.status_code == 200
    items = res.json()["items"]
    assert all(i["price"] >= 15 for i in items)

def test_get_products_sort(client, setup_data):
    res = client.get("/api/products?sort_by=price&sort_desc=true")
    assert res.status_code == 200
    items = res.json()["items"]
    prices = [i["price"] for i in items]
    assert prices == sorted(prices, reverse=True)

def test_get_product_detail(client, setup_data):
    p1 = setup_data["p1"]
    res = client.get(f"/api/products/{p1.id}")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == p1.id
    assert "category" in data
    assert "evidence" in data

def test_compare_products_valid(client, setup_data):
    p1 = setup_data["p1"]
    p2 = setup_data["p2"]
    res = client.post("/api/comparisons", json={"product_ids": [p1.id, p2.id]})
    assert res.status_code == 200
    data = res.json()
    assert len(data["items"]) == 2
    
def test_compare_products_invalid_len(client, setup_data):
    p1 = setup_data["p1"]
    res = client.post("/api/comparisons", json={"product_ids": [p1.id]})
    assert res.status_code == 400
    
def test_compare_products_duplicate(client, setup_data):
    p1 = setup_data["p1"]
    res = client.post("/api/comparisons", json={"product_ids": [p1.id, p1.id]})
    assert res.status_code == 400
