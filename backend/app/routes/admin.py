from flask import Blueprint, jsonify, request
from ..models import Lead, Scorecard, Interaction, db
from sqlalchemy import func, desc
import logging

logger = logging.getLogger(__name__)

admin_bp = Blueprint('admin', __name__)

# Simple auth middleware (replace with proper JWT in production)
def require_admin_key(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-Admin-Key')
        import os
        if api_key != os.getenv('ADMIN_API_KEY', 'admin-secret-key-change-me'):
            return {'error': 'Unauthorized'}, 401
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard', methods=['GET'])
@require_admin_key
def dashboard():
    """Admin dashboard with KPIs and metrics."""
    try:
        total_leads = db.session.query(func.count(Lead.id)).scalar()
        total_scorecards = db.session.query(func.count(Scorecard.id)).scalar()
        avg_score = db.session.query(func.avg(Scorecard.total_score)).scalar() or 0
        qualified_leads = db.session.query(func.count(Lead.id)).filter(Lead.lifecycle_stage == 'qualified').scalar()
        
        # Recent leads
        recent_leads = Lead.query.order_by(desc(Lead.created_at)).limit(10).all()
        
        # Top scores
        top_scores = db.session.query(Scorecard).order_by(desc(Scorecard.total_score)).limit(5).all()
        
        return jsonify({
            'metrics': {
                'total_leads': total_leads,
                'total_scorecards': total_scorecards,
                'avg_score': round(avg_score, 1),
                'qualified_leads': qualified_leads,
                'conversion_rate': round(qualified_leads / total_leads * 100, 1) if total_leads > 0 else 0
            },
            'recent_leads': [
                {
                    'id': l.id,
                    'email': l.email,
                    'company': l.company,
                    'stage': l.lifecycle_stage,
                    'score': l.lead_score,
                    'created_at': l.created_at.isoformat()
                } for l in recent_leads
            ],
            'top_scores': [
                {
                    'id': s.id,
                    'url': s.url,
                    'total_score': s.total_score,
                    'technical': s.technical_score,
                    'seo': s.seo_score,
                    'conversion': s.conversion_score,
                    'business': s.business_score
                } for s in top_scores
            ]
        }), 200
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        return {'error': str(e)}, 500

@admin_bp.route('/leads', methods=['GET'])
@require_admin_key
def list_leads():
    """List all leads with filtering and pagination."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        stage = request.args.get('stage', None)
        
        query = Lead.query
        if stage:
            query = query.filter_by(lifecycle_stage=stage)
        
        leads = query.order_by(desc(Lead.created_at)).paginate(page=page, per_page=per_page)
        
        return jsonify({
            'total': leads.total,
            'pages': leads.pages,
            'current_page': page,
            'leads': [
                {
                    'id': l.id,
                    'email': l.email,
                    'company': l.company,
                    'phone': l.phone,
                    'website': l.website,
                    'industry': l.industry,
                    'lead_score': l.lead_score,
                    'stage': l.lifecycle_stage,
                    'source': l.source,
                    'created_at': l.created_at.isoformat()
                } for l in leads.items
            ]
        }), 200
    except Exception as e:
        logger.error(f"List leads error: {e}")
        return {'error': str(e)}, 500

@admin_bp.route('/leads/<int:lead_id>', methods=['GET'])
@require_admin_key
def get_lead_detail(lead_id):
    """Get detailed lead information with scorecard history."""
    try:
        lead = Lead.query.get(lead_id)
        if not lead:
            return {'error': 'Lead not found'}, 404
        
        scorecards = Scorecard.query.filter_by(lead_id=lead_id).all()
        interactions = Interaction.query.filter_by(lead_id=lead_id).order_by(desc(Interaction.created_at)).all()
        
        return jsonify({
            'id': lead.id,
            'email': lead.email,
            'company': lead.company,
            'phone': lead.phone,
            'website': lead.website,
            'industry': lead.industry,
            'estimated_revenue': lead.estimated_revenue,
            'lead_score': lead.lead_score,
            'stage': lead.lifecycle_stage,
            'source': lead.source,
            'created_at': lead.created_at.isoformat(),
            'updated_at': lead.updated_at.isoformat(),
            'scorecards': [
                {
                    'id': s.id,
                    'url': s.url,
                    'total_score': s.total_score,
                    'created_at': s.created_at.isoformat()
                } for s in scorecards
            ],
            'interactions': [
                {
                    'event_type': i.event_type,
                    'metadata': i.metadata,
                    'created_at': i.created_at.isoformat()
                } for i in interactions
            ]
        }), 200
    except Exception as e:
        logger.error(f"Get lead detail error: {e}")
        return {'error': str(e)}, 500

@admin_bp.route('/analytics', methods=['GET'])
@require_admin_key
def analytics():
    """Analytics and reporting."""
    try:
        # Stage distribution
        stages = db.session.query(
            Lead.lifecycle_stage,
            func.count(Lead.id)
        ).group_by(Lead.lifecycle_stage).all()
        
        # Score distribution
        score_ranges = {
            'excellent': db.session.query(func.count(Scorecard.id)).filter(Scorecard.total_score >= 80).scalar(),
            'good': db.session.query(func.count(Scorecard.id)).filter((Scorecard.total_score >= 60) & (Scorecard.total_score < 80)).scalar(),
            'fair': db.session.query(func.count(Scorecard.id)).filter((Scorecard.total_score >= 40) & (Scorecard.total_score < 60)).scalar(),
            'poor': db.session.query(func.count(Scorecard.id)).filter(Scorecard.total_score < 40).scalar(),
        }
        
        # Source distribution
        sources = db.session.query(
            Lead.source,
            func.count(Lead.id)
        ).group_by(Lead.source).all()
        
        return jsonify({
            'stage_distribution': {stage: count for stage, count in stages},
            'score_distribution': score_ranges,
            'source_distribution': {source: count for source, count in sources}
        }), 200
    except Exception as e:
        logger.error(f"Analytics error: {e}")
        return {'error': str(e)}, 500
