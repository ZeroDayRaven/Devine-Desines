from flask import Blueprint, request, jsonify
from ..models import Interaction, Lead, db

track_bp = Blueprint('track', __name__)

@track_bp.route('/track', methods=['POST'])
def track_event():
    data = request.get_json()
    lead_id = data.get('lead_id')
    event_type = data.get('event_type')
    event_data = data.get('metadata', {})  # accept 'metadata' from frontend but store as event_data

    if not lead_id or not event_type:
        return jsonify({'error': 'Missing required fields'}), 400

    lead = Lead.query.get(lead_id)
    if not lead:
        return jsonify({'error': 'Lead not found'}), 404

    interaction = Interaction(lead_id=lead.id, event_type=event_type, event_data=event_data)
    db.session.add(interaction)
    db.session.commit()
    return jsonify({'status': 'ok'})
