import pytest
from app.models.category import Category
from app.models.product import Product

@pytest.fixture(scope="session")
def user_token(client, setup_data):
    res = client.post("/api/auth/login", json={"email": "test2@example.com", "password": "pass"})
    if res.status_code != 200:
        # Register first
        client.post("/api/auth/register", json={"name": "test", "email": "test2@example.com", "password": "pass"})
        res = client.post("/api/auth/login", json={"email": "test2@example.com", "password": "pass"})
    return res.json()["access_token"]

@pytest.fixture(scope="session")
def admin_token(client, db, setup_data):
    # Make user admin
    from app.models.user import User
    user = db.query(User).filter(User.email == "test2@example.com").first()
    user.role = "admin"
    db.commit()
    
    res = client.post("/api/auth/login", json={"email": "test2@example.com", "password": "pass"})
    return res.json()["access_token"]

def test_add_wishlist(client, setup_data, user_token):
    p = setup_data["p1"]
    res = client.post(
        "/api/wishlists",
        json={"product_id": p.id},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert res.status_code == 200

def test_add_wishlist_duplicate(client, setup_data, user_token):
    p = setup_data["p1"]
    res = client.post(
        "/api/wishlists",
        json={"product_id": p.id},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert res.status_code == 400

def test_get_wishlists(client, user_token):
    res = client.get(
        "/api/wishlists",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert res.status_code == 200
    assert len(res.json()) >= 1

def test_delete_wishlist(client, setup_data, user_token):
    p = setup_data["p1"]
    res = client.delete(
        f"/api/wishlists/{p.id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert res.status_code == 200

def test_admin_create_product(client, admin_token, setup_data):
    cat = setup_data["cat"]
    res = client.post(
        "/api/admin/products",
        json={"name": "Admin Product", "price": 100, "category_id": cat.id},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert res.status_code == 200
    assert res.json()["name"] == "Admin Product"

def test_admin_update_product(client, admin_token, setup_data):
    p = setup_data["p2"]
    res = client.patch(
        f"/api/admin/products/{p.id}",
        json={"price": 999},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert res.status_code == 200
    assert res.json()["price"] == 999

def test_admin_create_evidence(client, admin_token, setup_data):
    p = setup_data["p2"]
    res = client.post(
        "/api/admin/evidence",
        json={"product_id": p.id, "criterion": "durability"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert res.status_code == 200
    assert res.json()["verification_status"] == "pending"

def test_admin_verify_evidence(client, admin_token, setup_data):
    p = setup_data["p2"]
    ev_res = client.post(
        "/api/admin/evidence",
        json={"product_id": p.id, "criterion": "packaging"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    ev_id = ev_res.json()["id"]
    
    res = client.patch(
        f"/api/admin/evidence/{ev_id}/verification",
        json={"verification_status": "verified"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert res.status_code == 200
    assert res.json()["verification_status"] == "verified"
    
    # Check score recalculation via GET product
    prod_res = client.get(f"/api/products/{p.id}")
    assert prod_res.status_code == 200
    assert prod_res.json()["evidence_coverage"] > 0

def test_admin_delete_product(client, admin_token, setup_data):
    p = setup_data["p3"]
    res = client.delete(
        f"/api/admin/products/{p.id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert res.status_code == 200

def test_normal_user_admin_fail(client, user_token, db):
    from app.models.user import User
    # Demote to user for this test (since the previous test made it admin)
    user = db.query(User).filter(User.email == "test2@example.com").first()
    user.role = "user"
    db.commit()
    
    res = client.delete(
        f"/api/admin/products/1",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert res.status_code == 403

def test_comparisons_auth(client, user_token, setup_data):
    p1 = setup_data["p1"]
    p2 = setup_data["p2"]
    res = client.post(
        "/api/comparisons",
        json={"product_ids": [p1.id, p2.id]},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert res.status_code == 200
    comp_id = res.json()["id"]
    
    res2 = client.get(
        f"/api/comparisons/{comp_id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert res2.status_code == 200
