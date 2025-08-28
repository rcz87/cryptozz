#!/usr/bin/env python3
"""
Master GPT Schema Directory
Central directory for all specialized ChatGPT Custom GPT schemas.
Provides navigation and schema selection for different trading functions.
"""

from flask import Blueprint, jsonify

# Create blueprint for master schema directory
master_gpt_bp = Blueprint('master_gpt', __name__)

@master_gpt_bp.route('/', methods=['GET'])
def get_gpt_schemas_directory():
    """Master directory of all available GPT schemas"""
    
    return jsonify({
        "title": "Cryptocurrency Trading Platform - GPT Schemas Directory",
        "description": "Specialized OpenAPI schemas for different ChatGPT Custom GPT functions",
        "base_url": "https://gpts.guardiansofthetoken.id",
        "total_schemas": 5,
        "schemas": {
            "1_trading_signals": {
                "name": "Trading Signals & Analysis GPT",
                "description": "Core trading signals, SMC analysis, and signal scoring",
                "url": "/api/gpt-schemas/trading/openapi.json",
                "endpoints": 6,
                "specialization": "Trading signal generation and Smart Money Concept analysis",
                "use_cases": [
                    "Generate trading signals with confidence scoring",
                    "Analyze Smart Money Concept patterns",
                    "Get entry/exit points with risk management",
                    "Calculate signal quality scores"
                ]
            },
            "2_market_data": {
                "name": "Market Data & SMC Analysis GPT", 
                "description": "Real-time market data, order books, and technical analysis",
                "url": "/api/gpt-schemas/market/openapi.json",
                "endpoints": 6,
                "specialization": "Real-time market data and technical analysis",
                "use_cases": [
                    "Get real-time price and ticker data",
                    "Analyze order book depth and liquidity",
                    "Retrieve comprehensive market data",
                    "Identify SMC patterns and zones"
                ]
            },
            "3_monitoring": {
                "name": "System Monitoring & Performance GPT",
                "description": "System health monitoring and performance analytics", 
                "url": "/api/gpt-schemas/monitoring/openapi.json",
                "endpoints": 2,
                "specialization": "System monitoring and performance tracking",
                "use_cases": [
                    "Monitor system health and component status",
                    "Track performance metrics and response times",
                    "Analyze system reliability and uptime",
                    "Debug system issues and bottlenecks"
                ]
            },
            "4_analytics": {
                "name": "Advanced Analytics & Backtesting GPT",
                "description": "Strategy backtesting and performance analysis",
                "url": "/api/gpt-schemas/analytics/openapi.json", 
                "endpoints": 2,
                "specialization": "Strategy backtesting and quantitative analysis",
                "use_cases": [
                    "Run comprehensive strategy backtests",
                    "Analyze trading performance metrics",
                    "Optimize strategy parameters",
                    "Calculate risk-adjusted returns"
                ]
            },
            "5_news_telegram": {
                "name": "News Analysis & Telegram Integration GPT",
                "description": "News sentiment analysis and notification system",
                "url": "/api/gpt-schemas/news/openapi.json",
                "endpoints": 2,
                "specialization": "News analysis and notification management", 
                "use_cases": [
                    "Analyze cryptocurrency news sentiment",
                    "Send automated Telegram notifications",
                    "Track market-moving news events",
                    "Manage custom alert systems"
                ]
            }
        },
        "setup_instructions": {
            "step_1": "Choose a specialized GPT schema based on your use case",
            "step_2": "Copy the OpenAPI schema URL for your chosen specialization",
            "step_3": "Create a new ChatGPT Custom GPT at https://chat.openai.com/gpts/editor",
            "step_4": "Import the schema URL in the 'Actions' section",
            "step_5": "Configure the GPT's instructions based on the specialization"
        },
        "recommended_combinations": [
            {
                "name": "Complete Trading Suite",
                "schemas": ["trading_signals", "market_data"],
                "description": "Full trading analysis with signals and market data"
            },
            {
                "name": "System Administrator",
                "schemas": ["monitoring", "analytics"],
                "description": "Platform monitoring and performance analysis"
            },
            {
                "name": "News Trader",
                "schemas": ["trading_signals", "news_telegram"],
                "description": "News-driven trading with automated notifications"
            }
        ],
        "technical_details": {
            "openapi_version": "3.1.0",
            "authentication": "API Key (X-API-KEY header)",
            "max_endpoints_per_schema": 30,
            "response_format": "JSON",
            "base_domain": "gpts.guardiansofthetoken.id"
        }
    })

@master_gpt_bp.route('/count', methods=['GET'])
def get_schemas_summary():
    """Get summary of all schemas and endpoint counts"""
    
    return jsonify({
        "total_schemas": 5,
        "total_endpoints_distributed": 18,
        "schemas_breakdown": {
            "trading_signals": {"endpoints": 6, "focus": "Signal generation & SMC analysis"},
            "market_data": {"endpoints": 6, "focus": "Real-time data & technical analysis"},  
            "monitoring": {"endpoints": 2, "focus": "System health & performance"},
            "analytics": {"endpoints": 2, "focus": "Backtesting & strategy analysis"},
            "news_telegram": {"endpoints": 2, "focus": "News analysis & notifications"}
        },
        "chatgpt_compliance": "All schemas under 30 endpoint limit",
        "coverage": "18/124 core endpoints strategically distributed"
    })