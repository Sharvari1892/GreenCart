import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.category import Category
from app.models.product import Product
from app.models.sustainability_evidence import SustainabilityEvidence
from app.db.base import Base
from app.db.session import engine

def seed_data():
    db = SessionLocal()
    
    # Categories
    categories = [
        {"name": "Electronics", "description": "Sustainable electronics and gadgets"},
        {"name": "Clothing", "description": "Eco-friendly apparel"},
        {"name": "Home", "description": "Sustainable home goods"},
    ]
    
    for cat_data in categories:
        cat = db.query(Category).filter(Category.name == cat_data["name"]).first()
        if not cat:
            db.add(Category(**cat_data))
    db.commit()

    # Get categories
    cat_elec = db.query(Category).filter(Category.name == "Electronics").first()
    cat_cloth = db.query(Category).filter(Category.name == "Clothing").first()
    cat_home = db.query(Category).filter(Category.name == "Home").first()

    # Products
    products = [
        {
            "name": "Fairphone 5", "brand": "Fairphone", "description": "Modular, repairable smartphone.",
            "price": 699.00, "category_id": cat_elec.id, "durability_score": 90, "packaging_score": 85, "repairability_score": 100
        },
        {
            "name": "Eco Laptop Stand", "brand": "WoodWorks", "description": "Bamboo laptop stand.",
            "price": 35.00, "category_id": cat_elec.id, "durability_score": 95, "packaging_score": 90, "repairability_score": None
        },
        {
            "name": "Organic Cotton T-Shirt", "brand": "GreenThreads", "description": "100% organic cotton tee.",
            "price": 25.00, "category_id": cat_cloth.id, "durability_score": 80, "packaging_score": 95, "repairability_score": None
        },
        {
            "name": "Recycled Denim Jeans", "brand": "ReDenim", "description": "Jeans from recycled materials.",
            "price": 65.00, "category_id": cat_cloth.id, "durability_score": 85, "packaging_score": 80, "repairability_score": 75
        },
        {
            "name": "Bamboo Toothbrush", "brand": "SmileEco", "description": "Biodegradable toothbrush.",
            "price": 4.00, "category_id": cat_home.id, "durability_score": 50, "packaging_score": 100, "repairability_score": None
        },
        {
            "name": "Glass Food Containers", "brand": "PureStore", "description": "Set of 5 glass containers.",
            "price": 30.00, "category_id": cat_home.id, "durability_score": 90, "packaging_score": 85, "repairability_score": None
        },
        {
            "name": "Solar Power Bank", "brand": "SunCharge", "description": "10000mAh solar bank.",
            "price": 45.00, "category_id": cat_elec.id, "durability_score": 75, "packaging_score": 70, "repairability_score": 60
        },
        {
            "name": "Hemp Backpack", "brand": "NatureCarry", "description": "Durable hemp bag.",
            "price": 85.00, "category_id": cat_cloth.id, "durability_score": 95, "packaging_score": 90, "repairability_score": 80
        },
        {
            "name": "Reusable Silicone Bags", "brand": "ZipEco", "description": "Food storage bags.",
            "price": 15.00, "category_id": cat_home.id, "durability_score": 85, "packaging_score": 90, "repairability_score": None
        },
        {
            "name": "LED Smart Bulb", "brand": "EcoLight", "description": "Energy efficient bulb.",
            "price": 20.00, "category_id": cat_home.id, "durability_score": 80, "packaging_score": 75, "repairability_score": 40
        },
        {
            "name": "Refurbished Tablet", "brand": "TechRenew", "description": "Like-new tablet.",
            "price": 199.00, "category_id": cat_elec.id, "durability_score": 70, "packaging_score": 60, "repairability_score": 60
        },
        {
            "name": "Wool Sweaters", "brand": "WarmEarth", "description": "Ethically sourced wool.",
            "price": 120.00, "category_id": cat_cloth.id, "durability_score": 90, "packaging_score": 85, "repairability_score": 90
        },
        {
            "name": "Compostable Phone Case", "brand": "Pela", "description": "Zero waste case.",
            "price": 40.00, "category_id": cat_elec.id, "durability_score": 85, "packaging_score": 100, "repairability_score": None
        },
        {
            "name": "Stainless Steel Bottle", "brand": "HydroEco", "description": "Insulated bottle.",
            "price": 35.00, "category_id": cat_home.id, "durability_score": 100, "packaging_score": 80, "repairability_score": None
        },
        {
            "name": "Upcycled Sneakers", "brand": "TreadLight", "description": "Sneakers from ocean plastic.",
            "price": 95.00, "category_id": cat_cloth.id, "durability_score": 75, "packaging_score": 85, "repairability_score": 50
        }
    ]

    for prod_data in products:
        prod = db.query(Product).filter(Product.name == prod_data["name"]).first()
        if not prod:
            db.add(Product(**prod_data))
    db.commit()

    # Evidence (demo)
    fp = db.query(Product).filter(Product.name == "Fairphone 5").first()
    if fp:
        ev = db.query(SustainabilityEvidence).filter(SustainabilityEvidence.product_id == fp.id).first()
        if not ev:
            db.add(SustainabilityEvidence(
                product_id=fp.id,
                criterion="repairability",
                source_url="https://example.com/demo-evidence",
                description="Demonstration evidence for repairability score.",
                verification_status="verified"
            ))
            db.commit()

    db.close()
    print("Database seeded successfully.")

if __name__ == "__main__":
    seed_data()
