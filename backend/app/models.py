from . import db
from datetime import datetime

class Lead(db.Model):
    __tablename__ = 'leads'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(255), unique=True)
    phone = db.Column(db.String(20))
    whatsapp = db.Column(db.String(20))
    company = db.Column(db.String(255))
    website = db.Column(db.String(255))
    industry = db.Column(db.String(100))
    estimated_revenue = db.Column(db.Integer)
    employees = db.Column(db.Integer)
    location = db.Column(db.String(100))
    lead_score = db.Column(db.Integer, default=0)
    lifecycle_stage = db.Column(db.String(50), default='new')
    source = db.Column(db.String(50), default='scorecard')
    campaign = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Scorecard(db.Model):
    __tablename__ = 'scorecards'
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'))
    url = db.Column(db.String(255))
    total_score = db.Column(db.Integer)
    technical_score = db.Column(db.Integer)
    seo_score = db.Column(db.Integer)
    conversion_score = db.Column(db.Integer)
    business_score = db.Column(db.Integer)
    status = db.Column(db.String(20), default='processing')
    report_html = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ScorecardCheck(db.Model):
    __tablename__ = 'scorecard_checks'
    id = db.Column(db.Integer, primary_key=True)
    scorecard_id = db.Column(db.Integer, db.ForeignKey('scorecards.id'))
    category = db.Column(db.String(50))
    check_name = db.Column(db.String(100))
    passed = db.Column(db.Boolean)
    value = db.Column(db.Text)
    recommendation = db.Column(db.Text)
    weight = db.Column(db.Float, default=1.0)

class Interaction(db.Model):
    __tablename__ = 'interactions'
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'))
    event_type = db.Column(db.String(50))
    event_data = db.Column(db.JSON)  # renamed from metadata to avoid SQLAlchemy reserved name
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'))
    company = db.Column(db.String(255))
    package = db.Column(db.String(50))
    mrr = db.Column(db.Integer)
    launch_fee = db.Column(db.Integer)
    start_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='active')
    churn_date = db.Column(db.Date)
