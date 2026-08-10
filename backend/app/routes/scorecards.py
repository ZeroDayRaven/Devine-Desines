from flask import Blueprint, request, jsonify, current_app
from ..models import Lead, Scorecard, ScorecardCheck, Interaction, db
from ..services.scanner import scan_website
from ..services.scoring import calculate_scores
from ..services.email import send_scorecard_report, send_lead_notification
from ..services.lead_scoring import score_lead
from ..utils.security import validate_url
from ..utils.validators import is_valid_email
import logging

logger = logging.getLogger(__name__)

scorecards_bp = Blueprint('scorecards', __name__)

@scorecards_bp.route('/scorecards', methods=['POST'])
def create_scorecard():
    data = request.get_json()
    email = data.get('email')
    website = data.get('website')

    if not email or not website:
        return jsonify({'error': 'Email and website are required'}), 400
    if not is_valid_email(email):
        return jsonify({'error': 'Invalid email'}), 400
    if not validate_url(website):
        return jsonify({'error': 'Invalid or unsafe URL'}), 400

    if not website.startswith(('http://', 'https://')):
        website = 'https://' + website

    lead = Lead.query.filter_by(email=email).first()
    if not lead:
        lead = Lead(email=email, website=website, source='scorecard')
        db.session.add(lead)
        db.session.commit()
    else:
        lead.website = website
        db.session.commit()

    interaction = Interaction(lead_id=lead.id, event_type='scorecard_started')
    db.session.add(interaction)
    db.session.commit()

    try:
        scan_results = scan_website(website)
    except Exception as e:
        logger.error(f"Scan failed: {e}")
        return jsonify({'error': 'Could not scan website'}), 500

    scores = calculate_scores(scan_results)

    scorecard = Scorecard(
        lead_id=lead.id,
        url=website,
        total_score=scores['total'],
        technical_score=scores['technical'],
        seo_score=scores['seo'],
        conversion_score=scores['conversion'],
        business_score=scores['business'],
        status='completed'
    )
    db.session.add(scorecard)
    db.session.flush()

    for check in scan_results['checks']:
        sc = ScorecardCheck(
            scorecard_id=scorecard.id,
            category=check['category'],
            check_name=check['name'],
            passed=check['passed'],
            value=check.get('value', ''),
            recommendation=check.get('recommendation', ''),
            weight=check.get('weight', 1.0)
        )
        db.session.add(sc)
    db.session.commit()

    lead.lead_score = score_lead(lead, scorecard)
    lead.lifecycle_stage = 'qualified' if lead.lead_score >= 40 else 'new'
    db.session.commit()

    interaction = Interaction(lead_id=lead.id, event_type='scorecard_completed', event_data={'score': scorecard.total_score})
    db.session.add(interaction)
    db.session.commit()

    # Send emails
    send_scorecard_report(lead, scorecard)
    send_lead_notification(lead, scorecard)

    return jsonify({
        'scorecard_id': scorecard.id,
        'total_score': scorecard.total_score,
        'category_scores': {
            'technical': scorecard.technical_score,
            'seo': scorecard.seo_score,
            'conversion': scorecard.conversion_score,
            'business': scorecard.business_score
        },
        'lead_score': lead.lead_score,
        'stage': lead.lifecycle_stage,
        'lead_id': lead.id
    })
