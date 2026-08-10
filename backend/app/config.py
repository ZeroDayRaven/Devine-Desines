import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email (SendGrid)
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    SENDGRID_FROM_EMAIL = os.getenv('SENDGRID_FROM_EMAIL', 'info@devinedesignssa.com')
    
    # Analytics & Tracking
    ANALYTICS_CONSENT = os.getenv('ANALYTICS_CONSENT', 'false').lower() == 'true'
    GA_TRACKING_ID = os.getenv('GA_TRACKING_ID', '')
    FB_PIXEL_ID = os.getenv('FB_PIXEL_ID', '')
    
    # WhatsApp (Optional)
    WHATSAPP_API_KEY = os.getenv('WHATSAPP_API_KEY')
    WHATSAPP_PHONE_ID = os.getenv('WHATSAPP_PHONE_ID', '')
