#!/usr/bin/env python3
"""
Simple Trading Schema untuk ChatGPT Custom GPT
Versi minimal yang pasti bisa diimpor
"""

from flask import Blueprint, jsonify

# Create blueprint
simple_trading_bp = Blueprint('simple_trading', __name__)

@simple_trading_bp.route('/openapi.json', methods=['GET'])
def get_simple_trading_schema():
    """Simple OpenAPI schema optimized for ChatGPT import"""
    
    schema = {
        "openapi": "3.1.0",
        "info": {
            "title": "Simple Crypto Trading API",
            "description": "Simple cryptocurrency trading signals API",
            "version": "1.0.0"
        },
        "servers": [
            {
                "url": "https://f52957b0-5f4b-420e-8f0d-660133cb6c42-00-3p8q833h0k02m.worf.replit.dev",
                "description": "Development Server"
            }
        ],
        "paths": {
            "/api/gpts/status": {
                "get": {
                    "operationId": "getStatus",
                    "summary": "Get system status",
                    "responses": {
                        "200": {
                            "description": "System status",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "status": {"type": "string"},
                                            "version": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/gpts/sinyal/tajam": {
                "post": {
                    "operationId": "getTradingSignal",
                    "summary": "Get trading signal",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "symbol": {"type": "string", "example": "BTC-USDT"},
                                        "timeframe": {"type": "string", "example": "1H"}
                                    },
                                    "required": ["symbol", "timeframe"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Trading signal",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "signal": {
                                                "type": "object",
                                                "properties": {
                                                    "direction": {"type": "string"},
                                                    "confidence": {"type": "number"},
                                                    "entry_price": {"type": "number"}
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "components": {
            "securitySchemes": {
                "ApiKeyAuth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "X-API-Key"
                }
            }
        },
        "security": [
            {"ApiKeyAuth": []}
        ]
    }
    
    return jsonify(schema)