from app.models.sustainability_evidence import SustainabilityEvidence
from typing import List, Optional, Tuple

def calculate_evidence_coverage(evidence_list: List[SustainabilityEvidence]) -> float:
    """
    Calculate the percentage of the three sustainability criteria 
    that have at least one verified evidence record.
    Criteria: durability, packaging, repairability
    """
    verified_criteria = set()
    for ev in evidence_list:
        if ev.verification_status == "verified" and ev.criterion in ["durability", "packaging", "repairability"]:
            verified_criteria.add(ev.criterion)
    
    return (len(verified_criteria) / 3.0) * 100.0

def calculate_overall_score(
    durability: Optional[int], 
    packaging: Optional[int], 
    repairability: Optional[int], 
    evidence_coverage: float
) -> Optional[float]:
    """
    Overall score = 0.35 × durability + 0.25 × packaging + 0.25 × repairability + 0.15 × evidence quality.
    If any of the three criterion scores is missing, return None.
    """
    if durability is None or packaging is None or repairability is None:
        return None
        
    score = 0.35 * durability + 0.25 * packaging + 0.25 * repairability + 0.15 * evidence_coverage
    return round(score, 2)
