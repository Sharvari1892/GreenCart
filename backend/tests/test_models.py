from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.models.wishlist import Wishlist
from app.models.comparison import Comparison, ComparisonItem
from app.models.sustainability_evidence import SustainabilityEvidence

def test_create_user(db):
    user = User(name="Test User", email="test@example.com", password_hash="hash")
    db.add(user)
    db.commit()
    db.refresh(user)
    assert user.id is not None
    assert user.email == "test@example.com"

def test_create_category(db):
    cat = Category(name="Electronics", description="Gadgets")
    db.add(cat)
    db.commit()
    db.refresh(cat)
    assert cat.id is not None
    assert cat.name == "Electronics"
