def calculate_scores(scan_results):
    categories = ['technical', 'seo', 'conversion', 'business']
    category_scores = {}

    for cat in categories:
        checks = [c for c in scan_results['checks'] if c['category'] == cat]
        if not checks:
            category_scores[cat] = 0
            continue
        total_weight = sum(c.get('weight', 1.0) for c in checks)
        if total_weight == 0:
            category_scores[cat] = 0
            continue
        total_score = sum((100 if c['passed'] else 0) * c.get('weight', 1.0) for c in checks)
        category_scores[cat] = round(total_score / total_weight)

    total = round(sum(category_scores.get(c, 0) for c in categories) / 4.0)
    return {
        'total': total,
        'technical': category_scores.get('technical', 0),
        'seo': category_scores.get('seo', 0),
        'conversion': category_scores.get('conversion', 0),
        'business': category_scores.get('business', 0)
    }