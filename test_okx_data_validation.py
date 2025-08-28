#!/usr/bin/env python3
"""
Unit Test untuk Verifikasi Data Input OKX API
Memastikan konsistensi parsing dan struktur data sesuai dokumentasi OKX
"""

import unittest
import sys
sys.path.append('.')

from core.okx_fetcher import OKXFetcher
from core.enhanced_okx_fetcher import EnhancedOKXFetcher
from datetime import datetime
import time


class TestOKXDataValidation(unittest.TestCase):
    """Unit test untuk validasi data OKX API"""
    
    def setUp(self):
        """Setup test environment"""
        self.okx = OKXFetcher()
        self.enhanced_okx = EnhancedOKXFetcher()
        self.test_symbols = ['BTC-USDT', 'ETH-USDT', 'SOL-USDT']
        self.test_timeframes = ['1m', '5m', '15m', '1H', '4H', '1D']
    
    def test_okx_fetcher_initialization(self):
        """Test OKX fetcher initialization"""
        self.assertIsNotNone(self.okx)
        self.assertEqual(self.okx.base_url, "https://www.okx.com")
        self.assertIsInstance(self.okx.authenticated, bool)
        self.assertIsInstance(self.okx.cache_ttl, (int, float))
    
    def test_historical_data_structure(self):
        """Test struktur data historical sesuai dokumentasi OKX"""
        symbol = 'BTC-USDT'
        timeframe = '1H'
        
        data = self.okx.get_historical_data(symbol, timeframe, limit=5)
        
        # Test response structure
        self.assertIsInstance(data, dict)
        self.assertIn('symbol', data)
        self.assertIn('timeframe', data)
        self.assertIn('candles', data)
        self.assertIn('count', data)
        self.assertIn('status', data)
        
        # Test candles structure
        candles = data.get('candles', [])
        self.assertGreater(len(candles), 0, "Should return at least 1 candle")
        
        # Test each candle structure
        for candle in candles:
            self.assertIsInstance(candle, dict)
            
            # Required fields sesuai dokumentasi OKX
            required_fields = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
            for field in required_fields:
                self.assertIn(field, candle, f"Missing required field: {field}")
            
            # Test data types
            self.assertIsInstance(candle['timestamp'], int, "Timestamp should be integer")
            self.assertIsInstance(candle['open'], (int, float), "Open should be numeric")
            self.assertIsInstance(candle['high'], (int, float), "High should be numeric")
            self.assertIsInstance(candle['low'], (int, float), "Low should be numeric")
            self.assertIsInstance(candle['close'], (int, float), "Close should be numeric")
            self.assertIsInstance(candle['volume'], (int, float), "Volume should be numeric")
            
            # Test OHLC logic
            self.assertGreaterEqual(candle['high'], candle['open'], "High should be >= Open")
            self.assertGreaterEqual(candle['high'], candle['close'], "High should be >= Close")
            self.assertLessEqual(candle['low'], candle['open'], "Low should be <= Open")
            self.assertLessEqual(candle['low'], candle['close'], "Low should be <= Close")
            self.assertGreaterEqual(candle['volume'], 0, "Volume should be >= 0")
    
    def test_multiple_symbols_consistency(self):
        """Test konsistensi struktur data across multiple symbols"""
        timeframe = '1H'
        results = {}
        
        for symbol in self.test_symbols[:2]:  # Test 2 symbols
            data = self.okx.get_historical_data(symbol, timeframe, limit=3)
            results[symbol] = data
        
        # Check all symbols return data
        for symbol, data in results.items():
            self.assertIsNotNone(data, f"No data for {symbol}")
            self.assertIn('candles', data, f"No candles for {symbol}")
            
            candles = data.get('candles', [])
            self.assertGreater(len(candles), 0, f"No candles returned for {symbol}")
        
        # Check consistency across symbols
        reference_symbol = list(results.keys())[0]
        reference_candle = results[reference_symbol]['candles'][0]
        reference_fields = set(reference_candle.keys())
        
        for symbol, data in results.items():
            candles = data.get('candles', [])
            if candles:
                candle_fields = set(candles[0].keys())
                self.assertEqual(reference_fields, candle_fields, 
                               f"Field mismatch between {reference_symbol} and {symbol}")
    
    def test_multiple_timeframes_consistency(self):
        """Test konsistensi struktur data across multiple timeframes"""
        symbol = 'BTC-USDT'
        results = {}
        
        for timeframe in self.test_timeframes[:3]:  # Test 3 timeframes
            data = self.okx.get_historical_data(symbol, timeframe, limit=3)
            results[timeframe] = data
        
        # Check all timeframes return data
        for timeframe, data in results.items():
            self.assertIsNotNone(data, f"No data for {timeframe}")
            self.assertIn('candles', data, f"No candles for {timeframe}")
        
        # Check consistency across timeframes
        reference_tf = list(results.keys())[0]
        reference_candle = results[reference_tf]['candles'][0]
        reference_fields = set(reference_candle.keys())
        
        for timeframe, data in results.items():
            candles = data.get('candles', [])
            if candles:
                candle_fields = set(candles[0].keys())
                self.assertEqual(reference_fields, candle_fields, 
                               f"Field mismatch between {reference_tf} and {timeframe}")
    
    def test_timestamp_validity(self):
        """Test validitas timestamp sesuai dokumentasi OKX"""
        symbol = 'BTC-USDT'
        timeframe = '1H'
        
        data = self.okx.get_historical_data(symbol, timeframe, limit=5)
        candles = data.get('candles', [])
        
        self.assertGreater(len(candles), 0, "Should return candles for timestamp test")
        
        current_time = int(time.time() * 1000)  # Current time in milliseconds
        
        for candle in candles:
            timestamp = candle['timestamp']
            
            # Test timestamp format (should be milliseconds)
            self.assertIsInstance(timestamp, int)
            self.assertGreater(timestamp, 1000000000000, "Timestamp should be in milliseconds")
            self.assertLess(timestamp, current_time + 86400000, "Timestamp should not be in future")
            
            # Convert to datetime to verify it's reasonable
            dt = datetime.fromtimestamp(timestamp / 1000)
            self.assertGreater(dt.year, 2020, "Timestamp should be recent")
    
    def test_ticker_data_structure(self):
        """Test struktur ticker data"""
        symbol = 'BTC-USDT'
        
        ticker = self.okx.get_ticker_data(symbol)
        
        self.assertIsInstance(ticker, dict)
        
        if 'error' not in ticker:
            # Required ticker fields
            required_fields = ['symbol', 'last_price', 'volume_24h', 'timestamp']
            for field in required_fields:
                self.assertIn(field, ticker, f"Missing ticker field: {field}")
            
            # Test data types
            self.assertIsInstance(ticker['last_price'], (int, float))
            self.assertIsInstance(ticker['volume_24h'], (int, float))
            self.assertIsInstance(ticker['timestamp'], int)
            
            # Test value ranges
            self.assertGreater(ticker['last_price'], 0, "Price should be positive")
            self.assertGreaterEqual(ticker['volume_24h'], 0, "Volume should be non-negative")
    
    def test_order_book_structure(self):
        """Test struktur order book data"""
        symbol = 'BTC-USDT'
        
        orderbook = self.okx.get_order_book(symbol, depth=10)
        
        self.assertIsInstance(orderbook, dict)
        
        if 'error' not in orderbook:
            # Required orderbook fields
            required_fields = ['bids', 'asks', 'timestamp']
            for field in required_fields:
                self.assertIn(field, orderbook, f"Missing orderbook field: {field}")
            
            # Test bids and asks structure
            bids = orderbook.get('bids', [])
            asks = orderbook.get('asks', [])
            
            if bids:
                for bid in bids[:3]:  # Test first 3 bids
                    self.assertIsInstance(bid, list)
                    self.assertEqual(len(bid), 2, "Bid should have [price, size]")
                    self.assertIsInstance(bid[0], (int, float), "Bid price should be numeric")
                    self.assertIsInstance(bid[1], (int, float), "Bid size should be numeric")
            
            if asks:
                for ask in asks[:3]:  # Test first 3 asks
                    self.assertIsInstance(ask, list)
                    self.assertEqual(len(ask), 2, "Ask should have [price, size]")
                    self.assertIsInstance(ask[0], (int, float), "Ask price should be numeric")
                    self.assertIsInstance(ask[1], (int, float), "Ask size should be numeric")
    
    def test_data_freshness(self):
        """Test apakah data yang diterima fresh (tidak stale)"""
        symbol = 'BTC-USDT'
        timeframe = '1m'
        
        data = self.okx.get_historical_data(symbol, timeframe, limit=2)
        candles = data.get('candles', [])
        
        self.assertGreater(len(candles), 0, "Should return candles for freshness test")
        
        # Get latest candle
        latest_candle = candles[0]  # OKX returns latest first
        latest_timestamp = latest_candle['timestamp']
        
        current_time = int(time.time() * 1000)
        time_diff = current_time - latest_timestamp
        
        # For 1m timeframe, latest candle should be within 5 minutes
        max_age = 5 * 60 * 1000  # 5 minutes in milliseconds
        self.assertLess(time_diff, max_age, 
                       f"Latest candle is too old: {time_diff/1000/60:.1f} minutes")


if __name__ == '__main__':
    print("🧪 RUNNING OKX DATA VALIDATION UNIT TESTS")
    print("=" * 50)
    
    # Run tests with detailed output
    unittest.main(verbosity=2, exit=False)
    
    print("\n✅ Unit tests completed!")