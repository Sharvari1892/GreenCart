from app.services.scoring_service import calculate_evidence_coverage, calculate_overall_score
from app.models.sustainability_evidence import SustainabilityEvidence

def test_calculate_evidence_coverage():
    ev_durability = SustainabilityEvidence(criterion="durability", verification_status="verified")
    ev_packaging = SustainabilityEvidence(criterion="packaging", verification_status="verified")
    ev_repairability_pending = SustainabilityEvidence(criterion="repairability", verification_status="pending")
    ev_packaging2 = SustainabilityEvidence(criterion="packaging", verification_status="verified")
    
    # 2 unique verified
    coverage = calculate_evidence_coverage([ev_durability, ev_packaging, ev_repairability_pending, ev_packaging2])
    assert round(coverage, 2) == 66.67
    
    # All 3
    ev_rep_ver = SustainabilityEvidence(criterion="repairability", verification_status="verified")
    coverage2 = calculate_evidence_coverage([ev_durability, ev_packaging, ev_rep_ver])
    assert round(coverage2, 2) == 100.00
    
    # 0 verified
    coverage3 = calculate_evidence_coverage([ev_repairability_pending])
    assert round(coverage3, 2) == 0.0

def test_calculate_overall_score():
    # Valid
    score = calculate_overall_score(80, 90, 70, 66.67)
    # 0.35*80 + 0.25*90 + 0.25*70 + 0.15*66.67 = 28 + 22.5 + 17.5 + 10 = 78.0005
    assert round(score, 2) == 78.0
    
    # Missing durability
    score2 = calculate_overall_score(None, 90, 70, 66.67)
    assert score2 is None

    # Missing packaging
    score3 = calculate_overall_score(80, None, 70, 66.67)
    assert score3 is None
    
    # Missing repairability
    score4 = calculate_overall_score(80, 90, None, 66.67)
    assert score4 is None
