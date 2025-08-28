#!/usr/bin/env python3
"""
GPT Schema #5: News Analysis & Telegram Integration
Specialized OpenAPI schema for ChatGPT Custom GPT focused on news sentiment analysis and Telegram notifications.
Max 30 endpoints for ChatGPT compliance.
"""

from flask import Blueprint, jsonify

news_telegram_gpt_bp = Blueprint('news_telegram_gpt', __name__)

@news_telegram_gpt_bp.route('/openapi.json', methods=['GET'])
def get_news_telegram_schema():
    """OpenAPI schema for News Analysis & Telegram Integration GPT"""
    
    schema = {
        "openapi": "3.1.0",
        "info": {
            "title": "Cryptocurrency News Analysis & Telegram Integration API",
            "description": """
📰 **NEWS ANALYSIS & TELEGRAM INTEGRATION GPT**

Real-time cryptocurrency news analysis and intelligent Telegram notification system. 
This GPT specializes in:

• Real-time cryptocurrency news aggregation and analysis
• AI-powered sentiment analysis of market-moving news
• Intelligent news filtering and relevance scoring
• Automated Telegram notifications for trading signals
• Custom alert system for price movements and news events
• Social media sentiment tracking and analysis
• Market event correlation with price movements
• Multi-language news processing and translation

Perfect for staying informed about market developments and receiving timely notifications about trading opportunities.
            """.strip(),
            "version": "3.1.0",
            "contact": {
                "name": "News & Telegram GPT API",
                "url": "https://gpts.guardiansofthetoken.id"
            }
        },
        "servers": [
            {
                "url": "https://gpts.guardiansofthetoken.id",
                "description": "Production News & Telegram API Server"
            },
            {
                "url": "https://f52957b0-5f4b-420e-8f0d-660133cb6c42-00-3p8q833h0k02m.worf.replit.dev",
                "description": "Development Server (Replit)"
            }
        ],
        "paths": {
            "/api/news/status": {
                "get": {
                    "operationId": "getNewsStatus",
                    "summary": "Get news analysis system status",
                    "description": "Returns status of news feeds, sentiment analysis, and notification systems",
                    "tags": ["News System"],
                    "responses": {
                        "200": {
                            "description": "News system status retrieved",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/NewsStatus"}
                                }
                            }
                        }
                    }
                }
            },
            "/api/telegram/status": {
                "get": {
                    "operationId": "getTelegramStatus",
                    "summary": "Get Telegram bot status",
                    "description": "Returns Telegram bot connectivity and notification system status",
                    "tags": ["Telegram"],
                    "responses": {
                        "200": {
                            "description": "Telegram status retrieved",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/TelegramStatus"}
                                }
                            }
                        }
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "NewsStatus": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string"},
                        "feeds_active": {"type": "integer"},
                        "latest_update": {"type": "string"}
                    }
                },
                "TelegramStatus": {
                    "type": "object",
                    "properties": {
                        "bot_active": {"type": "boolean"},
                        "chat_connected": {"type": "boolean"},
                        "notifications_sent": {"type": "integer"}
                    }
                }
            }
        },
        "tags": [
            {"name": "News System", "description": "News analysis and sentiment tracking"},
            {"name": "Telegram", "description": "Telegram bot and notifications"}
        ]
    }
    
    return jsonify(schema)