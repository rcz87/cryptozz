"""
GPT Schemas Module
Provides specialized OpenAPI schemas for different ChatGPT Custom GPT functions.
Each schema contains max 30 endpoints for ChatGPT compliance.
"""

from .trading_signals_schema import trading_gpt_bp
from .market_data_schema import market_data_gpt_bp  
from .monitoring_schema import monitoring_gpt_bp
from .analytics_schema import analytics_gpt_bp
from .news_telegram_schema import news_telegram_gpt_bp

__all__ = [
    'trading_gpt_bp',
    'market_data_gpt_bp', 
    'monitoring_gpt_bp',
    'analytics_gpt_bp',
    'news_telegram_gpt_bp'
]