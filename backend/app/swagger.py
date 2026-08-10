from flask import Blueprint, jsonify
from flasgger import Flasgger

def register_swagger(app):
    """Register Swagger/OpenAPI documentation."""
    swagger = Flasgger(app, config={
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api/docs"
    })
    
    return swagger

def get_swagger_config():
    """Get Swagger/OpenAPI configuration."""
    return {
        "swagger": "2.0",
        "info": {
            "title": "Devine Designs API",
            "version": "1.0.0",
            "description": "Digital Asset Scorecard & Lead Management API"
        },
        "host": "localhost:5000",
        "basePath": "/api",
        "schemes": ["http", "https"],
        "consumes": ["application/json"],
        "produces": ["application/json"],
        "paths": {
            "/scorecards": {
                "post": {
                    "summary": "Create Website Scorecard",
                    "description": "Scan a website and generate a digital asset scorecard",
                    "tags": ["Scorecards"],
                    "parameters": [
                        {
                            "in": "body",
                            "name": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "email": {"type": "string", "example": "user@example.com"},
                                    "website": {"type": "string", "example": "https://example.com"}
                                },
                                "required": ["email", "website"]
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Scorecard created successfully",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "scorecard_id": {"type": "integer"},
                                    "total_score": {"type": "integer"},
                                    "category_scores": {"type": "object"},
                                    "lead_score": {"type": "integer"},
                                    "stage": {"type": "string"},
                                    "lead_id": {"type": "integer"}
                                }
                            }
                        },
                        "400": {"description": "Invalid email or website"},
                        "429": {"description": "Rate limit exceeded"}
                    }
                }
            },
            "/track": {
                "post": {
                    "summary": "Track User Event",
                    "description": "Record user interaction event",
                    "tags": ["Tracking"],
                    "parameters": [
                        {
                            "in": "body",
                            "name": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "lead_id": {"type": "integer"},
                                    "event_type": {"type": "string"},
                                    "metadata": {"type": "object"}
                                },
                                "required": ["lead_id", "event_type"]
                            }
                        }
                    ],
                    "responses": {
                        "200": {"description": "Event tracked"},
                        "400": {"description": "Missing required fields"},
                        "404": {"description": "Lead not found"}
                    }
                }
            },
            "/health": {
                "get": {
                    "summary": "Health Check",
                    "description": "API health status",
                    "tags": ["System"],
                    "responses": {
                        "200": {
                            "description": "API is healthy",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "status": {"type": "string"}
                                }
                            }
                        }
                    }
                }
            },
            "/ready": {
                "get": {
                    "summary": "Readiness Check",
                    "description": "Database connectivity status",
                    "tags": ["System"],
                    "responses": {
                        "200": {"description": "Ready to serve"},
                        "503": {"description": "Not ready"}
                    }
                }
            }
        },
        "securityDefinitions": {
            "AdminKey": {
                "type": "apiKey",
                "name": "X-Admin-Key",
                "in": "header"
            }
        }
    }
