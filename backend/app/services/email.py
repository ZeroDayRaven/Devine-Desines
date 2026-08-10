import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import current_app

logger = logging.getLogger(__name__)

def send_email(to_email, subject, html_content):
    """Send email via SendGrid with API key from app config."""
    api_key = current_app.config.get('SENDGRID_API_KEY')
    from_email = current_app.config.get('SENDGRID_FROM_EMAIL', 'info@devinedesignssa.com')
    
    if not api_key:
        logger.info(f"SendGrid API key not configured, would send to {to_email}: {subject}")
        return False
    
    try:
        message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=subject,
            html_content=html_content
        )
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        logger.info(f"Email sent to {to_email}, status {response.status_code}")
        return True
    except Exception as e:
        logger.error(f"Email failed: {e}")
        return False

def send_scorecard_report(lead, scorecard):
    """Send scorecard report to lead email."""
    html = f"""
    <h1>Your Digital Asset Scorecard</h1>
    <p>Hi {lead.email},</p>
    <p>Thank you for taking our Digital Asset assessment. Here's your personalized scorecard:</p>
    <h2>Overall Score: {scorecard.total_score}/100</h2>
    <ul>
        <li>Technical Score: {scorecard.technical_score}/100</li>
        <li>SEO Score: {scorecard.seo_score}/100</li>
        <li>Conversion Score: {scorecard.conversion_score}/100</li>
        <li>Business Score: {scorecard.business_score}/100</li>
    </ul>
    <p>Next steps: Schedule a strategy call with our team to discuss your results.</p>
    <p>Best regards,<br>Devine Designs Team</p>
    """
    return send_email(lead.email, "Your Digital Asset Scorecard", html)

def send_lead_notification(lead, scorecard):
    """Send internal notification that a new lead submitted scorecard."""
    admin_email = current_app.config.get('SENDGRID_FROM_EMAIL', 'info@devinedesignssa.com')
    html = f"""
    <h2>New Lead Scorecard Submission</h2>
    <p><strong>Email:</strong> {lead.email}</p>
    <p><strong>Website:</strong> {lead.website}</p>
    <p><strong>Score:</strong> {scorecard.total_score}/100</p>
    <p><strong>Lead Score:</strong> {lead.lead_score}/100</p>
    <p><strong>Stage:</strong> {lead.lifecycle_stage}</p>
    """
    return send_email(admin_email, f"New Lead: {lead.email}", html)
