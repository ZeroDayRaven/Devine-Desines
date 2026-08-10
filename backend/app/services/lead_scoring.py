def score_lead(lead, scorecard):
    score = 0
    if lead.estimated_revenue:
        if lead.estimated_revenue >= 5000000:
            score += 30
        elif lead.estimated_revenue >= 1000000:
            score += 20
        elif lead.estimated_revenue >= 500000:
            score += 10
    if lead.industry in ['law', 'real_estate', 'medical']:
        score += 10
    if scorecard.total_score < 40:
        score += 15
    elif scorecard.total_score < 60:
        score += 10
    else:
        score += 5
    return min(score, 100)