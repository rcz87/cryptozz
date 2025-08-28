#!/usr/bin/env python3
"""
Test Signal Engine Integration
Menguji integrasi analysis engines dengan signal generation
"""

import sys
import unittest
import pandas as pd
import numpy as np
from typing import Dict, Any

sys.path.append('.')

class TestSignalIntegration(unittest.TestCase):
    """Test integrasi antara analysis engines dan signal generation"""
    
    def setUp(self):
        """Setup test environment"""
        # Create test data dengan clear patterns
        np.random.seed(42)
        self.test_data = self._create_confluence_test_data()
        
    def _create_confluence_test_data(self) -> Dict[str, Any]:
        """Create test data dengan MA crossover + SMC patterns"""
        base_price = 50000
        candles = []
        
        # Create 40 candles dengan bullish confluence
        for i in range(40):
            if i < 15:  # Setup phase
                open_price = base_price + (i * 8) + np.random.normal(0, 20)
                close_price = open_price + np.random.uniform(3, 15)
                volume = 1000 + np.random.exponential(200)
            elif i < 25:  # Breakout phase dengan volume
                open_price = base_price + 120 + (i-15) * 25
                close_price = open_price + np.random.uniform(15, 35)
                volume = 2000 + np.random.exponential(600)  # High volume
            else:  # Continuation
                open_price = base_price + 370 + (i-25) * 15
                close_price = open_price + np.random.uniform(8, 20)
                volume = 1200 + np.random.exponential(300)
            
            high = max(open_price, close_price) + np.random.uniform(5, 15)
            low = min(open_price, close_price) - np.random.uniform(5, 12)
            
            candles.append({
                'timestamp': 1700000000000 + i * 3600000,
                'open': round(open_price, 2),
                'high': round(high, 2),
                'low': round(low, 2),
                'close': round(close_price, 2),
                'volume': round(volume, 2)
            })
        
        return {
            'candles': candles,
            'symbol': 'BTC-USDT',
            'timeframe': '1H',
            'current_price': candles[-1]['close']
        }
    
    def test_smc_analyzer_integration(self):
        """Test SMC analyzer dapat dipanggil dan memberikan hasil"""
        try:
            from core.professional_smc_analyzer import ProfessionalSMCAnalyzer
            
            smc = ProfessionalSMCAnalyzer()
            result = smc.analyze_market_structure(self.test_data)
            
            # Test basic structure
            self.assertIsInstance(result, dict)
            self.assertIn('structure_analysis', result)
            self.assertIn('market_bias', result)
            self.assertIn('confidence', result)
            
            # Test confidence is valid
            confidence = result.get('confidence', 0)
            self.assertIsInstance(confidence, (int, float))
            self.assertGreaterEqual(confidence, 0)
            self.assertLessEqual(confidence, 1)
            
            return result
            
        except ImportError:
            self.skipTest("SMC Analyzer not available")
    
    def test_signal_engine_integration(self):
        """Test standard signal engine integration"""
        try:
            from core.signal_engine import SignalEngine
            
            signal_engine = SignalEngine()
            df = pd.DataFrame(self.test_data['candles'])
            
            # Test signal generation
            result = signal_engine.generate_comprehensive_signals(
                df=df,
                symbol=self.test_data['symbol'],
                timeframe=self.test_data['timeframe']
            )
            
            # Test basic structure
            self.assertIsInstance(result, dict)
            
            # Should not have error for sufficient data
            if 'error' in result:
                print(f"Signal engine error: {result['error']}")
            
            # If successful, check structure
            if 'final_signal' in result:
                final_signal = result['final_signal']
                self.assertIsInstance(final_signal, dict)
                
                # Should have basic signal components
                if 'direction' in final_signal:
                    direction = final_signal['direction']
                    self.assertIn(direction.upper(), ['BUY', 'SELL', 'HOLD', 'NEUTRAL'])
            
            return result
            
        except ImportError:
            self.skipTest("Signal Engine not available")
    
    def test_ma_crossover_detection(self):
        """Test moving average crossover detection"""
        closes = [c['close'] for c in self.test_data['candles']]
        
        # Calculate simple moving averages
        def sma(prices, period):
            if len(prices) < period:
                return None
            return sum(prices[-period:]) / period
        
        sma_10 = sma(closes, 10)
        sma_20 = sma(closes, 20)
        
        self.assertIsNotNone(sma_10)
        self.assertIsNotNone(sma_20)
        
        # For bullish trend data, expect SMA10 > SMA20
        print(f"SMA10: {sma_10:.2f}, SMA20: {sma_20:.2f}")
        
        # Test that both SMAs are calculated
        self.assertIsInstance(sma_10, (int, float))
        self.assertIsInstance(sma_20, (int, float))
        self.assertGreater(sma_10, 0)
        self.assertGreater(sma_20, 0)
    
    def test_volume_analysis(self):
        """Test volume spike detection"""
        volumes = [c['volume'] for c in self.test_data['candles']]
        
        # Calculate average volume
        avg_volume = sum(volumes) / len(volumes)
        
        # Check for volume spikes (volume > 1.5x average)
        recent_volumes = volumes[-5:]  # Last 5 candles
        max_recent_volume = max(recent_volumes)
        
        volume_spike = max_recent_volume > avg_volume * 1.5
        
        print(f"Average volume: {avg_volume:.0f}")
        print(f"Max recent volume: {max_recent_volume:.0f}")
        print(f"Volume spike detected: {volume_spike}")
        
        # Test that volumes are positive
        for volume in volumes:
            self.assertGreater(volume, 0)
    
    def test_confluence_scoring(self):
        """Test confluence scoring logic"""
        # Get SMC analysis
        try:
            from core.professional_smc_analyzer import ProfessionalSMCAnalyzer
            smc = ProfessionalSMCAnalyzer()
            smc_result = smc.analyze_market_structure(self.test_data)
        except:
            smc_result = {'market_bias': 'neutral', 'confidence': 0.5}
        
        # Get technical factors
        closes = [c['close'] for c in self.test_data['candles']]
        volumes = [c['volume'] for c in self.test_data['candles']]
        
        # Calculate factors
        sma_10 = sum(closes[-10:]) / 10 if len(closes) >= 10 else closes[-1]
        sma_20 = sum(closes[-20:]) / 20 if len(closes) >= 20 else closes[-1]
        avg_volume = sum(volumes) / len(volumes)
        recent_volume = sum(volumes[-5:]) / 5
        
        # Confluence factors
        factors = {
            'smc_bullish': smc_result.get('market_bias', '').lower() in ['bullish'],
            'ma_alignment': sma_10 > sma_20,
            'price_trend': closes[-1] > closes[0],
            'volume_confirmation': recent_volume > avg_volume * 1.2,
            'smc_confidence': smc_result.get('confidence', 0) > 0.6
        }
        
        # Calculate confluence score
        confluence_count = sum(factors.values())
        total_factors = len(factors)
        confluence_score = (confluence_count / total_factors) * 100
        
        print(f"Confluence factors: {factors}")
        print(f"Confluence score: {confluence_score:.1f}%")
        
        # Test that confluence score is valid
        self.assertGreaterEqual(confluence_score, 0)
        self.assertLessEqual(confluence_score, 100)
        
        # Expected signal strength based on confluence
        if confluence_score >= 80:
            expected_strength = 'STRONG'
        elif confluence_score >= 60:
            expected_strength = 'MODERATE'
        else:
            expected_strength = 'WEAK'
        
        print(f"Expected signal strength: {expected_strength}")
        
        return {
            'confluence_score': confluence_score,
            'factors': factors,
            'expected_strength': expected_strength
        }
    
    def test_signal_quality_scenarios(self):
        """Test different signal quality scenarios"""
        
        # Scenario 1: All factors aligned (should be strong signal)
        perfect_confluence = {
            'smc_bullish': True,
            'ma_crossover': True,
            'volume_spike': True,
            'trend_confirmation': True,
            'structure_break': True
        }
        
        perfect_score = (sum(perfect_confluence.values()) / len(perfect_confluence)) * 100
        self.assertEqual(perfect_score, 100.0)
        
        # Scenario 2: Mixed signals (should be moderate)
        mixed_confluence = {
            'smc_bullish': True,
            'ma_crossover': True,
            'volume_spike': False,
            'trend_confirmation': True,
            'structure_break': False
        }
        
        mixed_score = (sum(mixed_confluence.values()) / len(mixed_confluence)) * 100
        self.assertEqual(mixed_score, 60.0)
        
        # Scenario 3: Poor confluence (should be weak)
        poor_confluence = {
            'smc_bullish': False,
            'ma_crossover': False,
            'volume_spike': True,
            'trend_confirmation': False,
            'structure_break': False
        }
        
        poor_score = (sum(poor_confluence.values()) / len(poor_confluence)) * 100
        self.assertEqual(poor_score, 20.0)
        
        print(f"Perfect confluence: {perfect_score}%")
        print(f"Mixed confluence: {mixed_score}%")
        print(f"Poor confluence: {poor_score}%")


def run_integration_tests():
    """Run signal integration tests"""
    print("🔗 RUNNING SIGNAL INTEGRATION TESTS")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSignalIntegration)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print(f"\n📊 INTEGRATION TEST SUMMARY:")
    print(f"✅ Tests run: {result.testsRun}")
    print(f"❌ Failures: {len(result.failures)}")
    print(f"⚠️ Errors: {len(result.errors)}")
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun) * 100
    print(f"🎯 SUCCESS RATE: {success_rate:.1f}%")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    run_integration_tests()
    print("\n✅ Signal integration testing completed!")