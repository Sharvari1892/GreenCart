import pytest
from app.models.category import Category
from app.models.product import Product
from app.models.user import User



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


