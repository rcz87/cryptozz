#!/usr/bin/env python3
"""
Performance Monitor & Logging Enhancement
Comprehensive monitoring untuk semua trading analysis modules
"""

import time
import logging
import sys
import threading
from datetime import datetime
from typing import Dict, List, Any
import functools
import psutil
import gc

sys.path.append('.')

class PerformanceMonitor:
    """Enhanced performance monitoring dengan detailed metrics"""
    
    def __init__(self):
        self.metrics = {}
        self.operation_times = {}
        self.memory_snapshots = {}
        self.bottlenecks = []
        
        # Setup detailed logging
        self.setup_enhanced_logging()
        
    def setup_enhanced_logging(self):
        """Setup comprehensive logging untuk semua modules"""
        
        # Configure detailed logging format
        detailed_formatter = logging.Formatter(
            '%(asctime)s | %(name)-30s | %(levelname)-8s | %(funcName)-20s | %(message)s'
        )
        
        # Add file handler for comprehensive logs
        file_handler = logging.FileHandler('trading_performance.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        
        # Console handler dengan metrics
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(detailed_formatter)
        
        # Add handlers to key modules
        modules_to_monitor = [
            'core.okx_fetcher',
            'core.professional_smc_analyzer', 
            'core.signal_generator',
            'core.multi_timeframe_analyzer',
            'core.enhanced_sharp_signal_engine',
            'core.institutional_signal_engine',
            'core.scoring_service',
            'gpts_routes'
        ]
        
        for module_name in modules_to_monitor:
            logger = logging.getLogger(module_name)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(file_handler)
            
        print(f"✅ Enhanced logging setup untuk {len(modules_to_monitor)} modules")
    
    def timing_decorator(self, operation_name: str):
        """Decorator untuk measure execution time"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
                
                try:
                    result = func(*args, **kwargs)
                    
                    end_time = time.time()
                    end_memory = psutil.Process().memory_info().rss / 1024 / 1024
                    
                    execution_time = (end_time - start_time) * 1000  # ms
                    memory_delta = end_memory - start_memory
                    
                    # Log performance metrics
                    logger = logging.getLogger(func.__module__)
                    logger.info(f"PERFORMANCE | {operation_name} | {execution_time:.1f}ms | Memory: {memory_delta:+.1f}MB")
                    
                    # Store metrics
                    if operation_name not in self.operation_times:
                        self.operation_times[operation_name] = []
                    
                    self.operation_times[operation_name].append({
                        'time': execution_time,
                        'memory_delta': memory_delta,
                        'timestamp': datetime.now()
                    })
                    
                    # Check for bottlenecks
                    if execution_time > 1000:  # Slower than 1 second
                        self.bottlenecks.append({
                            'operation': operation_name,
                            'time': execution_time,
                            'function': func.__name__,
                            'timestamp': datetime.now()
                        })
                        logger.warning(f"BOTTLENECK DETECTED | {operation_name} | {execution_time:.1f}ms")
                    
                    return result
                    
                except Exception as e:
                    end_time = time.time()
                    execution_time = (end_time - start_time) * 1000
                    
                    logger = logging.getLogger(func.__module__)
                    logger.error(f"ERROR | {operation_name} | {execution_time:.1f}ms | Error: {str(e)}")
                    
                    raise
                    
            return wrapper
        return decorator
    
    def monitor_data_processing(self, data_source: str, data_count: int, operation: str):
        """Monitor data processing metrics"""
        logger = logging.getLogger('data_processing')
        logger.info(f"DATA_PROCESSING | {data_source} | {operation} | {data_count} records")
        
        if data_source not in self.metrics:
            self.metrics[data_source] = {'total_processed': 0, 'operations': []}
        
        self.metrics[data_source]['total_processed'] += data_count
        self.metrics[data_source]['operations'].append({
            'operation': operation,
            'count': data_count,
            'timestamp': datetime.now()
        })
    
    def monitor_signal_generation(self, symbol: str, signal_type: str, confidence: float, processing_time: float):
        """Monitor signal generation metrics"""
        logger = logging.getLogger('signal_metrics')
        logger.info(f"SIGNAL_GENERATED | {symbol} | {signal_type} | Confidence: {confidence:.2f} | Time: {processing_time:.1f}ms")
        
        if 'signals' not in self.metrics:
            self.metrics['signals'] = []
        
        self.metrics['signals'].append({
            'symbol': symbol,
            'type': signal_type,
            'confidence': confidence,
            'processing_time': processing_time,
            'timestamp': datetime.now()
        })
    
    def monitor_api_calls(self, api_name: str, endpoint: str, response_time: float, status: str):
        """Monitor external API call performance"""
        logger = logging.getLogger('api_monitoring')
        logger.info(f"API_CALL | {api_name} | {endpoint} | {response_time:.1f}ms | {status}")
        
        if 'api_calls' not in self.metrics:
            self.metrics['api_calls'] = {}
        
        if api_name not in self.metrics['api_calls']:
            self.metrics['api_calls'][api_name] = []
        
        self.metrics['api_calls'][api_name].append({
            'endpoint': endpoint,
            'response_time': response_time,
            'status': status,
            'timestamp': datetime.now()
        })
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Generate comprehensive performance summary"""
        summary = {
            'operation_times': {},
            'bottlenecks': len(self.bottlenecks),
            'data_processing': self.metrics.get('data_processing', {}),
            'signal_metrics': len(self.metrics.get('signals', [])),
            'api_performance': {}
        }
        
        # Summarize operation times
        for operation, times in self.operation_times.items():
            if times:
                avg_time = sum(t['time'] for t in times) / len(times)
                max_time = max(t['time'] for t in times)
                min_time = min(t['time'] for t in times)
                
                summary['operation_times'][operation] = {
                    'count': len(times),
                    'avg_time_ms': round(avg_time, 1),
                    'max_time_ms': round(max_time, 1),
                    'min_time_ms': round(min_time, 1)
                }
        
        # Summarize API performance
        api_calls = self.metrics.get('api_calls', {})
        for api_name, calls in api_calls.items():
            if calls:
                avg_response = sum(c['response_time'] for c in calls) / len(calls)
                success_rate = sum(1 for c in calls if c['status'] == 'success') / len(calls)
                
                summary['api_performance'][api_name] = {
                    'total_calls': len(calls),
                    'avg_response_ms': round(avg_response, 1),
                    'success_rate': round(success_rate * 100, 1)
                }
        
        return summary
    
    def profile_function(self, func, *args, **kwargs):
        """Profile specific function execution"""
        import cProfile
        import pstats
        import io
        
        profiler = cProfile.Profile()
        profiler.enable()
        
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        profiler.disable()
        
        # Get profiling stats
        stream = io.StringIO()
        ps = pstats.Stats(profiler, stream=stream)
        ps.sort_stats('cumulative')
        ps.print_stats(10)  # Top 10 functions
        
        profile_output = stream.getvalue()
        
        logger = logging.getLogger('profiling')
        logger.info(f"PROFILING | {func.__name__} | Total time: {(end_time - start_time)*1000:.1f}ms")
        logger.debug(f"PROFILING DETAILS:\n{profile_output}")
        
        return result, profile_output


def setup_performance_monitoring():
    """Setup global performance monitoring"""
    monitor = PerformanceMonitor()
    
    # Add timing decorators to key functions (example implementation)
    print("🚀 Performance monitoring setup completed")
    print("📊 Monitoring features enabled:")
    print("   ✅ Execution time tracking")
    print("   ✅ Memory usage monitoring") 
    print("   ✅ Bottleneck detection")
    print("   ✅ Data processing metrics")
    print("   ✅ Signal generation tracking")
    print("   ✅ API call performance")
    print("   ✅ Function profiling")
    
    return monitor


if __name__ == '__main__':
    monitor = setup_performance_monitoring()
    
    # Test monitoring capabilities
    print("\n🧪 Testing monitoring capabilities...")
    
    # Simulate some operations
    import requests
    import time
    
    try:
        # Test API monitoring
        start = time.time()
        response = requests.get('http://localhost:5000/api/gpts/status', timeout=5)
        end = time.time()
        
        monitor.monitor_api_calls(
            'gpts_api', 
            '/status', 
            (end - start) * 1000, 
            'success' if response.status_code == 200 else 'error'
        )
        
        # Test signal monitoring
        start = time.time()
        signal_response = requests.post(
            'http://localhost:5000/api/gpts/sinyal/tajam',
            json={'symbol': 'BTC-USDT', 'timeframe': '1H'},
            timeout=15
        )
        end = time.time()
        
        if signal_response.status_code == 200:
            data = signal_response.json()
            signal_data = data.get('signal', {})
            
            monitor.monitor_signal_generation(
                'BTC-USDT',
                signal_data.get('direction', 'unknown'),
                signal_data.get('confidence', 0),
                (end - start) * 1000
            )
        
        # Generate performance summary
        summary = monitor.get_performance_summary()
        
        print("\n📊 PERFORMANCE SUMMARY:")
        print("=" * 25)
        for category, data in summary.items():
            if data:
                print(f"{category}: {data}")
        
        print("\n✅ Performance monitoring test completed!")
        
    except Exception as e:
        print(f"❌ Monitoring test failed: {e}")