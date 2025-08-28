#!/usr/bin/env python3
"""
GPT Schema #3: System Monitoring & Performance
Specialized OpenAPI schema for ChatGPT Custom GPT focused on system monitoring and performance tracking.
Max 30 endpoints for ChatGPT compliance.
"""

from flask import Blueprint, jsonify

monitoring_gpt_bp = Blueprint('monitoring_gpt', __name__)

@monitoring_gpt_bp.route('/openapi.json', methods=['GET'])
def get_monitoring_schema():
    """OpenAPI schema for System Monitoring & Performance GPT"""
    
    schema = {
        "openapi": "3.1.0",
        "info": {
            "title": "Cryptocurrency Trading System Monitoring & Performance API",
            "description": """
🔍 **SYSTEM MONITORING & PERFORMANCE GPT**

Comprehensive system monitoring and performance analytics for cryptocurrency trading platform. 
This GPT specializes in:

• Real-time system health monitoring and diagnostics
• Performance metrics tracking and optimization
• API endpoint status and response time monitoring
• Database connection and query performance analysis
• Signal generation performance and accuracy tracking
• Error tracking and debugging assistance
• Resource utilization monitoring
• Trading performance analytics and reporting

Perfect for system administrators, developers, and traders who need insights into platform performance and reliability.
            """.strip(),
            "version": "3.1.0",
            "contact": {
                "name": "Monitoring GPT API",
                "url": "https://gpts.guardiansofthetoken.id"
            }
        },
        "servers": [
            {
                "url": "https://gpts.guardiansofthetoken.id",
                "description": "Production Monitoring API Server"
            },
            {
                "url": "https://f52957b0-5f4b-420e-8f0d-660133cb6c42-00-3p8q833h0k02m.worf.replit.dev",
                "description": "Development Server (Replit)"
            }
        ],
        "paths": {
            "/health": {
                "get": {
                    "operationId": "getSystemHealth",
                    "summary": "Get comprehensive system health status",
                    "description": "Returns detailed system health including database, APIs, and component status",
                    "tags": ["Health Monitoring"],
                    "responses": {
                        "200": {
                            "description": "System health retrieved successfully",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/SystemHealth"}
                                }
                            }
                        }
                    }
                }
            },
            "/api/performance/stats": {
                "get": {
                    "operationId": "getPerformanceStats",
                    "summary": "Get system performance statistics",
                    "description": "Returns performance metrics including response times, throughput, and resource usage",
                    "tags": ["Performance"],
                    "responses": {
                        "200": {
                            "description": "Performance statistics retrieved successfully",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/PerformanceStats"}
                                }
                            }
                        }
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "SystemHealth": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "enum": ["healthy", "degraded", "unhealthy"]},
                        "components": {
                            "type": "object",
                            "properties": {
                                "database": {"type": "object"},
                                "okx_api": {"type": "object"},
                                "signal_generator": {"type": "object"}
                            }
                        },
                        "timestamp": {"type": "string"}
                    }
                },
                "PerformanceStats": {
                    "type": "object",
                    "properties": {
                        "response_times": {"type": "object"},
                        "throughput": {"type": "object"},
                        "error_rates": {"type": "object"}
                    }
                }
            }
        },
        "tags": [
            {"name": "Health Monitoring", "description": "System health and status monitoring"},
            {"name": "Performance", "description": "Performance metrics and analytics"}
        ]
    }
    
    return jsonify(schema)