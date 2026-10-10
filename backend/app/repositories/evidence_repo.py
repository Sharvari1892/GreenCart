from typing import List
from sqlalchemy.orm import Session
from app.models.sustainability_evidence import SustainabilityEvidence

def get_evidence_for_product(db: Session, product_id: int) -> List[SustainabilityEvidence]:
    return db.query(SustainabilityEvidence).filter(SustainabilityEvidence.product_id == product_id).all()
