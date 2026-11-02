import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.base import Base
from app.api.deps import get_db
from app.core.config import settings

# Explicitly declare isolated test environment
settings.ENVIRONMENT = "test"

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="session")
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="session")
def setup_data(db):
    from app.models.user import User
    from app.models.category import Category
    from app.models.product import Product
    from app.core.security import get_password_hash
    user = User(name="Test User", email="test2@example.com", password_hash=get_password_hash("pass"))
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
