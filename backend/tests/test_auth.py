import pytest
from app.models.user import User

def test_register(client, db):
    res = client.post("/api/auth/register", json={
        "name": "New User",
        "email": "new@example.com",
        "password": "pass"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["email"] == "new@example.com"
    assert "password" not in data
    assert "password_hash" not in data

def test_register_duplicate(client, db):
    res = client.post("/api/auth/register", json={
        "name": "New User 2",
        "email": "new@example.com",
        "password": "pass"
    })
    assert res.status_code == 400

def test_login(client, db):
    res = client.post("/api/auth/login", json={
        "email": "new@example.com",
        "password": "pass"
    })
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert "refresh_token" in data

def test_login_invalid(client, db):
    res = client.post("/api/auth/login", json={
        "email": "new@example.com",
        "password": "wrong"
    })
    assert res.status_code == 400

def test_refresh_token(client, db):
    # Login first
    login_res = client.post("/api/auth/login", json={
        "email": "new@example.com",
        "password": "pass"
    })
    tokens = login_res.json()
    
    # Refresh
    refresh_res = client.post("/api/auth/refresh", json={
        "refresh_token": tokens["refresh_token"]
    })
    assert refresh_res.status_code == 200
    data = refresh_res.json()
    assert "access_token" in data
    assert data["refresh_token"] != tokens["refresh_token"]

def test_logout(client, db):
    login_res = client.post("/api/auth/login", json={
        "email": "new@example.com",
        "password": "pass"
    })
    tokens = login_res.json()
    
    # Logout
    logout_res = client.post("/api/auth/logout", json={
        "refresh_token": tokens["refresh_token"]
    })
    assert logout_res.status_code == 200
    
    # Try refresh again
    refresh_res = client.post("/api/auth/refresh", json={
        "refresh_token": tokens["refresh_token"]
    })
    assert refresh_res.status_code == 401

def test_me(client, db):
    login_res = client.post("/api/auth/login", json={
        "email": "new@example.com",
        "password": "pass"
    })
    tokens = login_res.json()
    access_token = tokens["access_token"]
    
    res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 200
    assert res.json()["email"] == "new@example.com"
    
def test_me_unauthorized(client, db):
    res = client.get("/api/auth/me")
    assert res.status_code == 401
