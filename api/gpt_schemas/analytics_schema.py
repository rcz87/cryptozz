#!/usr/bin/env python3
"""
GPT Schema #4: Advanced Analytics & Backtesting
Specialized OpenAPI schema for ChatGPT Custom GPT focused on advanced analytics and backtesting capabilities.
Max 30 endpoints for ChatGPT compliance.
"""

from flask import Blueprint, jsonify

analytics_gpt_bp = Blueprint('analytics_gpt', __name__)

@analytics_gpt_bp.route('/openapi.json', methods=['GET'])
def get_analytics_schema():
    """OpenAPI schema for Advanced Analytics & Backtesting GPT"""
    
    schema = {
        "openapi": "3.1.0",
        "info": {
            "title": "Cryptocurrency Advanced Analytics & Backtesting API",
            "description": """
📈 **ADVANCED ANALYTICS & BACKTESTING GPT**

Professional-grade analytics and backtesting platform for cryptocurrency trading strategies. 
This GPT specializes in:

• Historical strategy backtesting with realistic market conditions
• Performance analytics and risk assessment
• Portfolio optimization and allocation strategies
• Advanced statistical analysis and correlation studies
• Machine learning model performance tracking
• Strategy comparison and benchmarking
• Risk metrics calculation (Sharpe ratio, maximum drawdown, etc.)
• Monte Carlo simulations and stress testing

Perfect for quantitative analysts, strategy developers, and professional traders seeking comprehensive performance analysis.
            """.strip(),
            "version": "3.1.0",
            "contact": {
                "name": "Analytics GPT API",
                "url": "https://gpts.guardiansofthetoken.id"
            }
        },
        "servers": [
            {
                "url": "https://gpts.guardiansofthetoken.id",
                "description": "Production Analytics API Server"
            },
            {
                "url": "https://f52957b0-5f4b-420e-8f0d-660133cb6c42-00-3p8q833h0k02m.worf.replit.dev",
                "description": "Development Server (Replit)"
            }
        ],
        "paths": {
            "/api/backtest": {
                "post": {
                    "operationId": "runBacktest",
                    "summary": "Run strategy backtest",
                    "description": "Execute comprehensive backtesting of trading strategies with historical data",
                    "tags": ["Backtesting"],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "strategy": {"type": "string"},
                                        "symbol": {"type": "string"},
                                        "start_date": {"type": "string"},
                                        "end_date": {"type": "string"},
                                        "initial_capital": {"type": "number"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Backtest completed successfully",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/BacktestResults"}
                                }
                            }
                        }
                    }
                }
            },
            "/api/backtest/quick": {
                "post": {
                    "operationId": "runQuickBacktest",
                    "summary": "Run quick strategy validation",
                    "description": "Fast backtesting for strategy validation and parameter optimization",
                    "tags": ["Backtesting"],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "strategy_params": {"type": "object"},
                                        "symbol": {"type": "string"},
                                        "period": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Quick backtest completed",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/QuickBacktestResults"}
                                }
                            }
                        }
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "BacktestResults": {
                    "type": "object",
                    "properties": {
                        "strategy_name": {"type": "string"},
                        "performance": {
                            "type": "object",
                            "properties": {
                                "total_return": {"type": "number"},
                                "sharpe_ratio": {"type": "number"},
                                "max_drawdown": {"type": "number"},
                                "win_rate": {"type": "number"}
                            }
                        },
                        "trades": {"type": "array"},
                        "equity_curve": {"type": "array"}
                    }
                },
                "QuickBacktestResults": {
                    "type": "object",
                    "properties": {
                        "success_rate": {"type": "number"},
                        "profit_loss": {"type": "number"},
                        "risk_metrics": {"type": "object"}
                    }
                }
            }
        },
        "tags": [
            {"name": "Backtesting", "description": "Strategy backtesting and validation"}
        ]
    }
    
    return jsonify(schema)