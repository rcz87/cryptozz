#!/usr/bin/env python3
"""
GPT Schema #1: Trading Signals & Analysis
Specialized OpenAPI schema for ChatGPT Custom GPT focused on core trading signals and analysis.
Max 30 endpoints for ChatGPT compliance.
"""

from flask import Blueprint, jsonify

# Create blueprint for trading signals schema
trading_gpt_bp = Blueprint('trading_gpt', __name__)

@trading_gpt_bp.route('/openapi.json', methods=['GET'])
def get_trading_signals_schema():
    """OpenAPI schema for Trading Signals & Analysis GPT"""
    
    schema = {
        "openapi": "3.1.0",
        "info": {
            "title": "Cryptocurrency Trading Signals & Analysis API",
            "description": """
🎯 **TRADING SIGNALS & ANALYSIS GPT**

Advanced AI-powered cryptocurrency trading signals with professional Smart Money Concept (SMC) analysis. 
This GPT specializes in:

• Real-time trading signal generation with confidence scoring
• Smart Money Concept (SMC) pattern recognition and analysis
• Multi-timeframe technical analysis (1m to 1M)
• Risk management calculations and position sizing
• Entry/exit point identification with stop-loss and take-profit levels
• Market structure analysis and trend identification
• Signal performance tracking and optimization

Perfect for traders seeking institutional-grade trading intelligence with AI-powered insights.
            """.strip(),
            "version": "3.1.0",
            "contact": {
                "name": "Trading Signals GPT API",
                "url": "https://gpts.guardiansofthetoken.id"
            }
        },
        "servers": [
            {
                "url": "https://f52957b0-5f4b-420e-8f0d-660133cb6c42-00-3p8q833h0k02m.worf.replit.dev",
                "description": "Replit Development Server"
            }
        ],
        "paths": {
            # Core Trading Signals
            "/api/gpts/status": {
                "get": {
                    "operationId": "getSystemStatus",
                    "summary": "Get trading system status and capabilities",
                    "description": "Returns overall system health, supported symbols, timeframes, and component status",
                    "tags": ["System Status"],
                    "responses": {
                        "200": {
                            "description": "System status retrieved successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "status": {"type": "string", "example": "healthy"},
                                            "version": {"type": "string", "example": "3.1.0"},
                                            "components": {
                                                "type": "object",
                                                "properties": {
                                                    "okx_api": {"type": "string", "example": "connected"},
                                                    "database": {"type": "string", "example": "connected"},
                                                    "ai_engine": {"type": "string", "example": "ready"}
                                                },
                                                "additionalProperties": True
                                            },
                                            "supported_symbols": {
                                                "type": "array",
                                                "items": {"type": "string"},
                                                "example": ["BTC-USDT", "ETH-USDT"]
                                            }
                                        },
                                        "additionalProperties": True
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/gpts/sinyal/tajam": {
                "post": {
                    "operationId": "getSharpTradingSignal",
                    "summary": "Generate sharp trading signal with AI analysis",
                    "description": "Generates high-confidence trading signals using SMC analysis, technical indicators, and AI reasoning",
                    "tags": ["Trading Signals"],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "symbol": {"type": "string", "example": "BTCUSDT", "description": "Trading pair symbol"},
                                        "timeframe": {"type": "string", "enum": ["1m", "5m", "15m", "1H", "4H", "1D"], "example": "1H"},
                                        "enhanced_ai": {"type": "boolean", "default": False, "description": "Enable AI-enhanced analysis"}
                                    },
                                    "required": ["symbol", "timeframe"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Trading signal generated successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/TradingSignal"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/gpts/smc-analysis": {
                "post": {
                    "operationId": "getSmcAnalysis",
                    "summary": "Get Smart Money Concept analysis",
                    "description": "Performs comprehensive SMC analysis including order blocks, fair value gaps, and market structure",
                    "tags": ["SMC Analysis"],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "symbol": {"type": "string", "example": "BTCUSDT"},
                                        "timeframe": {"type": "string", "enum": ["15m", "1H", "4H", "1D"], "example": "1H"}
                                    },
                                    "required": ["symbol", "timeframe"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "SMC analysis completed successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/SmcAnalysis"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/gpts/smc-zones/{symbol}": {
                "get": {
                    "operationId": "getSmcZones",
                    "summary": "Get SMC zones for symbol",
                    "description": "Returns order blocks, fair value gaps, and liquidity zones for the specified symbol",
                    "tags": ["SMC Analysis"],
                    "parameters": [
                        {
                            "name": "symbol",
                            "in": "path",
                            "required": True,
                            "description": "Trading pair symbol",
                            "schema": {"type": "string", "example": "BTCUSDT"}
                        },
                        {
                            "name": "timeframe",
                            "in": "query",
                            "description": "Timeframe for analysis",
                            "schema": {"type": "string", "enum": ["15m", "1H", "4H", "1D"], "default": "1H"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "SMC zones retrieved successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/SmcZones"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/sharp/score/{symbol}": {
                "get": {
                    "operationId": "getSharpScore",
                    "summary": "Get sharp signal scoring",
                    "description": "Returns quality score for trading signals with detailed breakdown",
                    "tags": ["Signal Scoring"],
                    "parameters": [
                        {
                            "name": "symbol",
                            "in": "path",
                            "required": True,
                            "description": "Trading pair symbol",
                            "schema": {"type": "string", "example": "BTCUSDT"}
                        },
                        {
                            "name": "timeframe",
                            "in": "query",
                            "description": "Analysis timeframe",
                            "schema": {"type": "string", "enum": ["15m", "1H", "4H", "1D"], "default": "1H"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Sharp score calculated successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/SharpScore"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/signal/enhanced/{symbol}": {
                "get": {
                    "operationId": "getEnhancedSignal",
                    "summary": "Get enhanced trading signal",
                    "description": "Returns enhanced signal with multi-factor analysis and confidence metrics",
                    "tags": ["Trading Signals"],
                    "parameters": [
                        {
                            "name": "symbol",
                            "in": "path",
                            "required": True,
                            "description": "Trading pair symbol",
                            "schema": {"type": "string", "example": "BTCUSDT"}
                        },
                        {
                            "name": "timeframe",
                            "in": "query",
                            "description": "Signal timeframe",
                            "schema": {"type": "string", "enum": ["15m", "1H", "4H", "1D"], "default": "1H"}
                        },
                        {
                            "name": "risk_level",
                            "in": "query",
                            "description": "Risk tolerance level",
                            "schema": {"type": "string", "enum": ["conservative", "moderate", "aggressive"], "default": "moderate"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Enhanced signal generated successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/EnhancedSignal"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "TradingSignal": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "example": "success"},
                        "signal": {
                            "type": "object",
                            "properties": {
                                "direction": {"type": "string", "enum": ["BUY", "SELL", "HOLD", "STRONG_BUY", "STRONG_SELL"]},
                                "confidence": {"type": "number", "minimum": 0, "maximum": 1, "description": "Signal confidence (0-1)"},
                                "entry_price": {"type": "number", "description": "Recommended entry price"},
                                "stop_loss": {"type": "number", "description": "Stop loss level"},
                                "take_profit": {"type": "number", "description": "Take profit target"},
                                "reasoning": {"type": "string", "description": "AI reasoning for the signal"}
                            }
                        },
                        "analysis": {
                            "type": "object",
                            "properties": {
                                "smc": {
                                    "type": "object",
                                    "properties": {
                                        "market_bias": {"type": "string", "enum": ["bullish", "bearish", "neutral"]},
                                        "structure_break": {"type": "string"},
                                        "confidence": {"type": "number"}
                                    }
                                },
                                "technical": {"type": "string", "description": "Technical analysis summary"},
                                "risk_reward": {"type": "number", "description": "Risk to reward ratio"}
                            }
                        },
                        "market_data": {
                            "type": "object",
                            "properties": {
                                "current_price": {"type": "number"},
                                "data_status": {"type": "string"},
                                "candles_analyzed": {"type": "integer"}
                            }
                        }
                    }
                },
                "SmcAnalysis": {
                    "type": "object",
                    "properties": {
                        "market_structure": {"type": "string"},
                        "trend_direction": {"type": "string"},
                        "key_levels": {
                            "type": "object",
                            "properties": {
                                "support": {"type": "array", "items": {"type": "number"}},
                                "resistance": {"type": "array", "items": {"type": "number"}}
                            }
                        },
                        "order_blocks": {"type": "array", "items": {"type": "object"}},
                        "fair_value_gaps": {"type": "array", "items": {"type": "object"}}
                    }
                },
                "SmcZones": {
                    "type": "object",
                    "properties": {
                        "zones": {
                            "type": "object",
                            "properties": {
                                "bullish_ob": {"type": "array", "items": {"type": "object"}},
                                "bearish_ob": {"type": "array", "items": {"type": "object"}},
                                "fvg": {"type": "array", "items": {"type": "object"}}
                            }
                        },
                        "zone_analysis": {
                            "type": "object",
                            "properties": {
                                "total_zones": {"type": "integer"},
                                "active_zones": {"type": "integer"},
                                "proximity_alerts": {"type": "array", "items": {"type": "object"}}
                            }
                        }
                    }
                },
                "SharpScore": {
                    "type": "object",
                    "properties": {
                        "total_score": {"type": "number", "minimum": 0, "maximum": 100},
                        "quality_rating": {"type": "string", "enum": ["EXCELLENT", "SHARP", "GOOD", "POOR"]},
                        "recommendation": {"type": "string", "enum": ["EXECUTE", "CONSIDER", "WATCH", "AVOID"]},
                        "score_breakdown": {
                            "type": "object",
                            "properties": {
                                "smc_score": {"type": "number"},
                                "technical_score": {"type": "number"},
                                "momentum_score": {"type": "number"},
                                "volume_score": {"type": "number"}
                            }
                        }
                    }
                },
                "EnhancedSignal": {
                    "type": "object",
                    "properties": {
                        "signal": {"$ref": "#/components/schemas/TradingSignal"},
                        "multi_timeframe": {
                            "type": "object",
                            "properties": {
                                "short_term": {"type": "string"},
                                "medium_term": {"type": "string"},
                                "long_term": {"type": "string"}
                            }
                        },
                        "risk_management": {
                            "type": "object",
                            "properties": {
                                "position_size": {"type": "number"},
                                "max_risk": {"type": "number"},
                                "risk_reward_ratio": {"type": "number"}
                            }
                        }
                    }
                }
            },
            "securitySchemes": {
                "ApiKeyAuth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "X-API-KEY"
                }
            }
        },
        "tags": [
            {"name": "System Status", "description": "System health and status endpoints"},
            {"name": "Trading Signals", "description": "Core trading signal generation"},
            {"name": "SMC Analysis", "description": "Smart Money Concept analysis"},
            {"name": "Signal Scoring", "description": "Signal quality scoring and metrics"}
        ]
    }
    
    return jsonify(schema)