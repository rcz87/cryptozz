#!/usr/bin/env python3
"""
GPT Schema #2: Market Data & SMC Analysis
Specialized OpenAPI schema for ChatGPT Custom GPT focused on real-time market data and SMC analysis.
Max 30 endpoints for ChatGPT compliance.
"""

from flask import Blueprint, jsonify

# Create blueprint for market data schema
market_data_gpt_bp = Blueprint('market_data_gpt', __name__)

@market_data_gpt_bp.route('/openapi.json', methods=['GET'])
def get_market_data_schema():
    """OpenAPI schema for Market Data & SMC Analysis GPT"""
    
    schema = {
        "openapi": "3.1.0",
        "info": {
            "title": "Cryptocurrency Market Data & SMC Analysis API",
            "description": """
📊 **MARKET DATA & SMC ANALYSIS GPT**

Real-time cryptocurrency market data with advanced Smart Money Concept analysis. 
This GPT specializes in:

• Real-time price feeds and market data from OKX authenticated API
• Order book analysis with institutional-grade depth data
• Smart Money Concept pattern recognition and visualization
• Market structure analysis and trend identification
• Volume profile analysis and Point of Control (POC) detection
• Multi-timeframe market data aggregation
• Technical indicator calculations and analysis
• Market sentiment and momentum tracking

Perfect for market analysis, chart reading, and understanding institutional money flow patterns.
            """.strip(),
            "version": "3.1.0",
            "contact": {
                "name": "Market Data GPT API",
                "url": "https://gpts.guardiansofthetoken.id"
            }
        },
        "servers": [
            {
                "url": "https://gpts.guardiansofthetoken.id",
                "description": "Production Market Data API Server"
            },
            {
                "url": "https://f52957b0-5f4b-420e-8f0d-660133cb6c42-00-3p8q833h0k02m.worf.replit.dev",
                "description": "Development Server (Replit)"
            }
        ],
        "paths": {
            # Real-time Market Data
            "/api/gpts/ticker/{symbol}": {
                "get": {
                    "operationId": "getRealtimeTicker",
                    "summary": "Get real-time ticker data",
                    "description": "Returns real-time price, volume, and 24h statistics for the specified symbol",
                    "tags": ["Market Data"],
                    "parameters": [
                        {
                            "name": "symbol",
                            "in": "path",
                            "required": True,
                            "description": "Trading pair symbol (e.g., BTCUSDT)",
                            "schema": {"type": "string", "example": "BTCUSDT"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Real-time ticker data retrieved successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/TickerData"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/gpts/orderbook/{symbol}": {
                "get": {
                    "operationId": "getOrderBook",
                    "summary": "Get order book depth data",
                    "description": "Returns real-time order book with bid/ask levels and liquidity depth",
                    "tags": ["Market Data"],
                    "parameters": [
                        {
                            "name": "symbol",
                            "in": "path",
                            "required": True,
                            "description": "Trading pair symbol",
                            "schema": {"type": "string", "example": "BTCUSDT"}
                        },
                        {
                            "name": "depth",
                            "in": "query",
                            "description": "Order book depth levels",
                            "schema": {"type": "integer", "enum": [5, 10, 20, 50], "default": 20}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Order book data retrieved successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/OrderBook"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/gpts/market-data": {
                "post": {
                    "operationId": "getMarketData",
                    "summary": "Get comprehensive market data",
                    "description": "Returns historical price data, volume analysis, and technical indicators",
                    "tags": ["Market Data"],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "symbol": {"type": "string", "example": "BTCUSDT"},
                                        "timeframe": {"type": "string", "enum": ["1m", "5m", "15m", "1H", "4H", "1D"], "example": "1H"},
                                        "limit": {"type": "integer", "minimum": 10, "maximum": 1000, "default": 100}
                                    },
                                    "required": ["symbol", "timeframe"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Market data retrieved successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/MarketData"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/smc/zones": {
                "get": {
                    "operationId": "getSmcZonesSummary",
                    "summary": "Get SMC zones summary",
                    "description": "Returns overview of all SMC zones across timeframes",
                    "tags": ["SMC Analysis"],
                    "parameters": [
                        {
                            "name": "symbol",
                            "in": "query",
                            "description": "Filter by symbol",
                            "schema": {"type": "string", "example": "BTCUSDT"}
                        },
                        {
                            "name": "timeframe",
                            "in": "query",
                            "description": "Filter by timeframe",
                            "schema": {"type": "string", "enum": ["15m", "1H", "4H", "1D"]}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "SMC zones summary retrieved successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/SmcZonesSummary"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/smc/pattern/{symbol}": {
                "get": {
                    "operationId": "getSmcPatterns",
                    "summary": "Get SMC pattern recognition",
                    "description": "Identifies SMC patterns like CHoCH, BOS, and structural breaks",
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
                            "description": "Analysis timeframe",
                            "schema": {"type": "string", "enum": ["15m", "1H", "4H", "1D"], "default": "1H"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "SMC patterns identified successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/SmcPatterns"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/chart/data/{symbol}": {
                "get": {
                    "operationId": "getChartData",
                    "summary": "Get chart data for visualization",
                    "description": "Returns formatted chart data suitable for visualization and analysis",
                    "tags": ["Chart Data"],
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
                            "description": "Chart timeframe",
                            "schema": {"type": "string", "enum": ["1m", "5m", "15m", "1H", "4H", "1D"], "default": "1H"}
                        },
                        {
                            "name": "indicators",
                            "in": "query",
                            "description": "Include technical indicators",
                            "schema": {"type": "boolean", "default": True}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Chart data retrieved successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/ChartData"
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
                "TickerData": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "example": "success"},
                        "ticker": {
                            "type": "object",
                            "properties": {
                                "symbol": {"type": "string", "example": "BTC-USDT"},
                                "last_price": {"type": "number", "description": "Current price"},
                                "bid_price": {"type": "number", "description": "Highest bid"},
                                "ask_price": {"type": "number", "description": "Lowest ask"},
                                "high_24h": {"type": "number", "description": "24h high"},
                                "low_24h": {"type": "number", "description": "24h low"},
                                "volume_24h": {"type": "number", "description": "24h volume"},
                                "change_24h": {"type": "number", "description": "24h price change %"},
                                "timestamp": {"type": "integer", "description": "Data timestamp"}
                            }
                        }
                    }
                },
                "OrderBook": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "example": "success"},
                        "orderbook": {
                            "type": "object",
                            "properties": {
                                "symbol": {"type": "string"},
                                "bids": {
                                    "type": "array",
                                    "description": "Buy orders [price, quantity]",
                                    "items": {
                                        "type": "array",
                                        "items": {"type": "number"}
                                    }
                                },
                                "asks": {
                                    "type": "array",
                                    "description": "Sell orders [price, quantity]",
                                    "items": {
                                        "type": "array",
                                        "items": {"type": "number"}
                                    }
                                },
                                "timestamp": {"type": "integer"}
                            }
                        }
                    }
                },
                "MarketData": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string"},
                        "data": {
                            "type": "object",
                            "properties": {
                                "symbol": {"type": "string"},
                                "timeframe": {"type": "string"},
                                "candles": {
                                    "type": "array",
                                    "description": "OHLCV data",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "timestamp": {"type": "integer"},
                                            "open": {"type": "number"},
                                            "high": {"type": "number"},
                                            "low": {"type": "number"},
                                            "close": {"type": "number"},
                                            "volume": {"type": "number"}
                                        }
                                    }
                                },
                                "indicators": {
                                    "type": "object",
                                    "properties": {
                                        "sma_20": {"type": "array", "items": {"type": "number"}},
                                        "ema_20": {"type": "array", "items": {"type": "number"}},
                                        "rsi": {"type": "array", "items": {"type": "number"}},
                                        "macd": {"type": "object"}
                                    }
                                }
                            }
                        }
                    }
                },
                "SmcZonesSummary": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string"},
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
                                "proximity_alerts": {"type": "array"}
                            }
                        }
                    }
                },
                "SmcPatterns": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string"},
                        "patterns": {
                            "type": "object",
                            "properties": {
                                "choch": {"type": "array", "description": "Change of Character patterns"},
                                "bos": {"type": "array", "description": "Break of Structure patterns"},
                                "liquidity_sweeps": {"type": "array"},
                                "order_blocks": {"type": "array"},
                                "fair_value_gaps": {"type": "array"}
                            }
                        },
                        "market_structure": {
                            "type": "object",
                            "properties": {
                                "trend": {"type": "string", "enum": ["bullish", "bearish", "neutral"]},
                                "structure_strength": {"type": "number"},
                                "key_levels": {"type": "array"}
                            }
                        }
                    }
                },
                "ChartData": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string"},
                        "chart": {
                            "type": "object",
                            "properties": {
                                "symbol": {"type": "string"},
                                "timeframe": {"type": "string"},
                                "ohlcv": {"type": "array"},
                                "volume_profile": {"type": "object"},
                                "technical_levels": {
                                    "type": "object",
                                    "properties": {
                                        "support": {"type": "array"},
                                        "resistance": {"type": "array"},
                                        "pivot_points": {"type": "array"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "tags": [
            {"name": "Market Data", "description": "Real-time market data and price feeds"},
            {"name": "SMC Analysis", "description": "Smart Money Concept pattern analysis"},
            {"name": "Chart Data", "description": "Chart visualization and technical data"}
        ]
    }
    
    return jsonify(schema)