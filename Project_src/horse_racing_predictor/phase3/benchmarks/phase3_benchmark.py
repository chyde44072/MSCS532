import time
import random
import statistics
import threading
import gc
from typing import List, Tuple, Dict, Any
import sys
import os
import json
from datetime import datetime

# Add parent directories to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
phase1_phase2_path = os.path.join(project_root, 'phase1_phase2')
shared_path = os.path.join(project_root, 'shared')
sys.path.insert(0, phase1_phase2_path)
sys.path.insert(0, shared_path)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Original implementations
from data_structures.hash_table import HorseDatabase
from data_structures.leaderboard_heap import Leaderboard
from data_structures.avl_tree import AVLTree

# Optimized implementations
from optimized_data_structures.optimized_hash_table import OptimizedHorseDatabase
from optimized_data_structures.optimized_leaderboard import OptimizedLeaderboard
from optimized_data_structures.optimized_avl_tree import OptimizedAVLTree


class SimplifiedBenchmarkSuite:
    """Comprehensive benchmarking suite for performance analysis without external dependencies."""
    
    def __init__(self):
        self.results = {}
        self.test_data_cache = {}
        
    def generate_large_dataset(self, size: int) -> Tuple[List[Tuple[str, dict]], List[Tuple[str, float]]]:
        """Generate large test dataset for scalability testing using built-in random."""
        if size in self.test_data_cache:
            return self.test_data_cache[size]
        
        print(f"Generating test dataset of size {size}...")
        horses = []
        race_times = []
        
        # Use different distributions for realistic data
        jockey_pool = [f"Jockey_{i}" for i in range(min(size // 10, 100))]
        
        for i in range(size):
            horse_id = f"H{i:08d}"
            
            # Generate realistic age distribution (3-10 years, average ~5)
            age = max(3, min(10, int(random.gauss(5, 1.5))))
            
            # Generate realistic win rate (beta-like distribution)
            win_rate = random.betavariate(2, 5)  # Skewed towards lower win rates
            
            # Generate speed (30-60 mph, average ~45)
            speed = max(30, min(60, random.gauss(45, 8)))
            
            wins = int(win_rate * 50)
            races = wins + random.randint(5, 30)
            
            horse_data = {
                "name": f"Horse_{i}",
                "age": age,
                "wins": wins,
                "races": races,
                "jockey": random.choice(jockey_pool),
                "avg_speed": round(speed, 1),
                "win_ratio": wins / races if races > 0 else 0
            }
            
            # Generate race time based on speed (inverse relationship)
            base_time = 120 - speed + random.uniform(-5, 5)
            race_time = max(55.0, round(base_time, 2))
            
            horses.append((horse_id, horse_data))
            race_times.append((horse_id, race_time))
        
        self.test_data_cache[size] = (horses, race_times)
        return horses, race_times
    
    def benchmark_hash_table_advanced(self, horses: List[Tuple[str, dict]], 
                                    operations: int = 1000) -> Dict[str, Any]:
        """Advanced hash table benchmarking with detailed metrics."""
        print("🔍 Advanced Hash Table Benchmarking...")
        
        # Test original implementation
        original_results = self._benchmark_hash_implementation(
            HorseDatabase(), horses, operations, "Original"
        )
        
        # Test optimized implementation with correct parameters
        optimized_results = self._benchmark_hash_implementation(
            OptimizedHorseDatabase(cache_size=min(2000, len(horses)), enable_indexing=True), 
            horses, operations, "Optimized"
        )
        
        return {
            'original': original_results,
            'optimized': optimized_results,
            'improvement': self._calculate_improvement(original_results, optimized_results)
        }
    
    def _benchmark_hash_implementation(self, db_instance, horses: List[Tuple[str, dict]], 
                                     operations: int, label: str) -> Dict[str, Any]:
        """Benchmark a specific hash table implementation."""
        results = {'label': label}
        
        # Bulk insertion test
        start_time = time.time()
        if hasattr(db_instance, 'add_horses_bulk'):
            db_instance.add_horses_bulk(horses)
        else:
            for horse_id, data in horses:
                db_instance.add_horse(horse_id, data)
        
        insert_time = time.time() - start_time
        results['bulk_insert_time'] = insert_time
        results['insert_rate'] = len(horses) / insert_time
        
        # Random lookup performance
        test_ids = random.sample([h[0] for h in horses], min(operations, len(horses)))
        lookup_times = []
        
        for horse_id in test_ids:
            start_time = time.time()
            result = db_instance.get_horse(horse_id)
            lookup_times.append(time.time() - start_time)
            
        results['avg_lookup_time'] = statistics.mean(lookup_times)
        results['lookup_std'] = statistics.stdev(lookup_times) if len(lookup_times) > 1 else 0
        results['lookup_rate'] = 1 / results['avg_lookup_time']
        
        # Bulk retrieval test (if available)
        if hasattr(db_instance, 'get_horses_bulk'):
            bulk_test_ids = random.sample([h[0] for h in horses], min(100, len(horses)))
            start_time = time.time()
            bulk_results = db_instance.get_horses_bulk(bulk_test_ids)
            bulk_time = time.time() - start_time
            results['bulk_retrieval_time'] = bulk_time
            results['bulk_retrieval_rate'] = len(bulk_test_ids) / bulk_time
        else:
            # Simulate bulk retrieval
            bulk_test_ids = random.sample([h[0] for h in horses], min(100, len(horses)))
            start_time = time.time()
            for horse_id in bulk_test_ids:
                db_instance.get_horse(horse_id)
            bulk_time = time.time() - start_time
            results['bulk_retrieval_time'] = bulk_time
            results['bulk_retrieval_rate'] = len(bulk_test_ids) / bulk_time
        
        # Index query performance (if supported)
        if hasattr(db_instance, 'find_horses_by_jockey'):
            jockey_query_times = []
            jockeys = list(set(h[1].get('jockey', '') for h in horses[:100]))
            
            for jockey in jockeys[:10]:
                start_time = time.time()
                results_jockey = db_instance.find_horses_by_jockey(jockey)
                jockey_query_times.append(time.time() - start_time)
            
            results['avg_index_query_time'] = statistics.mean(jockey_query_times)
            
        # Cache performance (if supported)
        if hasattr(db_instance, 'get_cache_stats'):
            cache_stats = db_instance.get_cache_stats()
            results['cache_stats'] = cache_stats
        
        # Memory efficiency
        if hasattr(db_instance, 'get_memory_usage_estimate'):
            memory_usage = db_instance.get_memory_usage_estimate()
            results['memory_breakdown'] = memory_usage
        
        return results
    
    def benchmark_leaderboard_advanced(self, race_times: List[Tuple[str, float]], 
                                     operations: int = 1000) -> Dict[str, Any]:
        """Advanced leaderboard benchmarking."""
        print("🏆 Advanced Leaderboard Benchmarking...")
        
        # Test original implementation
        original_results = self._benchmark_leaderboard_implementation(
            Leaderboard(), race_times, operations, "Original"
        )
        
        # Test optimized implementation with correct parameters
        optimized_results = self._benchmark_leaderboard_implementation(
            OptimizedLeaderboard(cache_top_k=min(50, len(race_times)//10)),
            race_times, operations, "Optimized"
        )
        
        return {
            'original': original_results,
            'optimized': optimized_results,
            'improvement': self._calculate_improvement(original_results, optimized_results)
        }
    
    def _benchmark_leaderboard_implementation(self, leaderboard_instance, 
                                            race_times: List[Tuple[str, float]], 
                                            operations: int, label: str) -> Dict[str, Any]:
        """Benchmark a specific leaderboard implementation."""
        results = {'label': label}
        
        # Bulk insertion
        start_time = time.time()
        if hasattr(leaderboard_instance, 'add_results_bulk'):
            leaderboard_instance.add_results_bulk(race_times)
        else:
            for horse_id, race_time in race_times:
                leaderboard_instance.add_result(horse_id, race_time)
        
        insert_time = time.time() - start_time
        results['bulk_insert_time'] = insert_time
        results['insert_rate'] = len(race_times) / insert_time
        
        # Top-k query performance
        topk_times = []
        k_values = [5, 10, 20, 50, 100]
        
        for k in k_values:
            if k <= leaderboard_instance.size():
                times_for_k = []
                for _ in range(min(100, operations // len(k_values))):
                    start_time = time.time()
                    leaderboard_instance.get_top_performers(k)
                    times_for_k.append(time.time() - start_time)
                topk_times.append((k, statistics.mean(times_for_k)))
        
        results['topk_performance'] = topk_times
        
        # Range query performance (if supported)
        if hasattr(leaderboard_instance, 'get_top_performers_in_time_range'):
            range_times = []
            for _ in range(min(50, operations // 4)):
                min_time = random.uniform(55, 70)
                max_time = min_time + random.uniform(5, 15)
                start_time = time.time()
                leaderboard_instance.get_top_performers_in_time_range(min_time, max_time, 10)
                range_times.append(time.time() - start_time)
            
            results['avg_range_query_time'] = statistics.mean(range_times)
        else:
            # Skip range queries if not available
            results['avg_range_query_time'] = None
        
        # Rank query performance
        rank_times = []
        test_ids = random.sample([rt[0] for rt in race_times], min(100, len(race_times)))
        
        for horse_id in test_ids:
            start_time = time.time()
            if hasattr(leaderboard_instance, 'get_horse_rank'):
                leaderboard_instance.get_horse_rank(horse_id)
            else:
                # Skip if method doesn't exist
                pass
            rank_times.append(time.time() - start_time)
        
        if rank_times:
            results['avg_rank_query_time'] = statistics.mean(rank_times)
        else:
            results['avg_rank_query_time'] = None
        
        # Performance stats (if available)
        if hasattr(leaderboard_instance, 'get_performance_stats'):
            performance_stats = leaderboard_instance.get_performance_stats()
            results['performance_stats'] = performance_stats
        
        return results
    
    def benchmark_avl_tree_advanced(self, horses: List[Tuple[str, dict]], 
                                  operations: int = 1000) -> Dict[str, Any]:
        """Advanced AVL tree benchmarking."""
        print("🌳 Advanced AVL Tree Benchmarking...")
        
        # Prepare win ratio data
        win_ratio_data = []
        for horse_id, data in horses:
            if data['races'] > 0:
                ratio = data['wins'] / data['races']
                win_ratio_data.append((horse_id, ratio))
        
        # Test original implementation
        original_results = self._benchmark_avl_implementation(
            AVLTree(), win_ratio_data, operations, "Original"
        )
        
        # Test optimized implementation with simplified parameters
        optimized_results = self._benchmark_avl_implementation(
            OptimizedAVLTree(),  # Use default constructor
            win_ratio_data, operations, "Optimized"
        )
        
        return {
            'original': original_results,
            'optimized': optimized_results,
            'improvement': self._calculate_improvement(original_results, optimized_results)
        }
    
    def _benchmark_avl_implementation(self, tree_instance, win_ratio_data: List[Tuple[str, float]], 
                                    operations: int, label: str) -> Dict[str, Any]:
        """Benchmark a specific AVL tree implementation."""
        results = {'label': label}
        
        # Bulk insertion
        start_time = time.time()
        if hasattr(tree_instance, 'insert_bulk'):
            tree_instance.insert_bulk(win_ratio_data)
        else:
            for horse_id, ratio in win_ratio_data:
                tree_instance.insert(horse_id, ratio)
        
        insert_time = time.time() - start_time
        results['bulk_insert_time'] = insert_time
        results['insert_rate'] = len(win_ratio_data) / insert_time
        
        # Range query performance
        range_times = []
        for _ in range(min(100, operations)):
            min_ratio = random.uniform(0.0, 0.5)
            max_ratio = min_ratio + random.uniform(0.1, 0.5)
            start_time = time.time()
            tree_instance.get_range(min_ratio, max_ratio)
            range_times.append(time.time() - start_time)
        
        results['avg_range_query_time'] = statistics.mean(range_times)
        results['range_query_std'] = statistics.stdev(range_times)
        
        # Rank query performance (if supported)
        if hasattr(tree_instance, 'get_rank'):
            rank_times = []
            test_ratios = [wr[1] for wr in random.sample(win_ratio_data, min(50, len(win_ratio_data)))]
            
            for ratio in test_ratios:
                start_time = time.time()
                tree_instance.get_rank(ratio)
                rank_times.append(time.time() - start_time)
            
            results['avg_rank_query_time'] = statistics.mean(rank_times)
        
        # K-th element queries (if supported)
        if hasattr(tree_instance, 'get_kth_smallest'):
            kth_times = []
            total_size = len(win_ratio_data)
            
            for _ in range(min(50, operations // 4)):
                k = random.randint(1, total_size)
                start_time = time.time()
                tree_instance.get_kth_smallest(k)
                kth_times.append(time.time() - start_time)
            
            results['avg_kth_query_time'] = statistics.mean(kth_times)
        
        # Sorted traversal performance (if available)
        if hasattr(tree_instance, 'get_sorted_list'):
            start_time = time.time()
            tree_instance.get_sorted_list()
            results['sorted_traversal_time'] = time.time() - start_time
        else:
            # Use in-order traversal alternative if available
            start_time = time.time()
            if hasattr(tree_instance, 'get_range'):
                # Get all elements using range query
                tree_instance.get_range(0.0, 1.0)
            results['sorted_traversal_time'] = time.time() - start_time
        
        # Tree statistics (if available)
        if hasattr(tree_instance, 'get_statistics'):
            tree_stats = tree_instance.get_statistics()
            results['tree_statistics'] = tree_stats
        
        return results
    
    def run_scalability_analysis(self, sizes: List[int] = None) -> Dict[str, Any]:
        """Run comprehensive scalability analysis."""
        if sizes is None:
            sizes = [1000, 5000, 10000, 25000]
        
        print("📈 Running Scalability Analysis...")
        scalability_results = {}
        
        for size in sizes:
            print(f"\\nTesting with {size:,} records...")
            horses, race_times = self.generate_large_dataset(size)
            
            # Limit operations for larger datasets to keep tests reasonable
            operations = min(1000, size // 10)
            
            size_results = {
                'hash_table': self.benchmark_hash_table_advanced(horses, operations),
                'leaderboard': self.benchmark_leaderboard_advanced(race_times, operations),
                'avl_tree': self.benchmark_avl_tree_advanced(horses, operations)
            }
            
            scalability_results[size] = size_results
            
            # Force garbage collection between tests
            gc.collect()
        
        return scalability_results
    
    def run_stress_tests(self) -> Dict[str, Any]:
        """Run stress tests under extreme conditions."""
        print("⚡ Running Stress Tests...")
        
        stress_results = {}
        
        # Concurrent access test
        stress_results['concurrent_access'] = self._test_concurrent_access()
        
        # Memory pressure test
        stress_results['memory_pressure'] = self._test_memory_pressure()
        
        # Extreme dataset sizes
        stress_results['extreme_sizes'] = self._test_extreme_sizes()
        
        return stress_results
    
    def _test_concurrent_access(self) -> Dict[str, Any]:
        """Test performance under concurrent access."""
        print("🔄 Testing concurrent access...")
        
        # Generate test data
        horses, race_times = self.generate_large_dataset(5000)
        
        # Setup optimized instances
        db = OptimizedHorseDatabase(cache_size=1000, enable_indexing=True)
        leaderboard = OptimizedLeaderboard(cache_top_k=50)
        
        # Populate with initial data
        initial_horses = [(h[0], h[1]) for h in horses[:2500]]
        db.add_horses_bulk(initial_horses)
        leaderboard.add_results_bulk(race_times[:2500])
        
        def worker_thread(thread_id: int, results: List):
            """Worker thread for concurrent testing."""
            thread_results = {'thread_id': thread_id, 'operations': 0, 'errors': 0}
            start_time = time.time()
            
            try:
                for i in range(100):
                    # Mix of read and write operations
                    if i % 3 == 0:
                        # Add new horse
                        horse_id, data = horses[2500 + thread_id * 100 + i]
                        db.add_horse(horse_id, data)
                        race_time = race_times[2500 + thread_id * 100 + i][1]
                        leaderboard.add_result(horse_id, race_time)
                    else:
                        # Read operations
                        test_horse = random.choice(horses[:2500])
                        db.get_horse(test_horse[0])
                        leaderboard.get_top_performers(10)
                    
                    thread_results['operations'] += 1
                    
            except Exception as e:
                thread_results['errors'] += 1
            
            thread_results['duration'] = time.time() - start_time
            results.append(thread_results)
        
        # Run concurrent threads
        num_threads = 8
        thread_results = []
        threads = []
        
        start_time = time.time()
        for i in range(num_threads):
            thread = threading.Thread(target=worker_thread, args=(i, thread_results))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        total_time = time.time() - start_time
        
        return {
            'num_threads': num_threads,
            'total_time': total_time,
            'thread_results': thread_results,
            'total_operations': sum(r['operations'] for r in thread_results),
            'total_errors': sum(r['errors'] for r in thread_results),
            'operations_per_second': sum(r['operations'] for r in thread_results) / total_time
        }
    
    def _test_memory_pressure(self) -> Dict[str, Any]:
        """Test performance under memory pressure."""
        print("💾 Testing memory pressure...")
        
        # Create large dataset that challenges memory
        large_horses, large_race_times = self.generate_large_dataset(50000)
        
        # Test memory usage with different configurations
        memory_results = {}
        
        # Test optimized vs original under memory pressure
        for impl_name, db_class in [('original', HorseDatabase), 
                                   ('optimized', OptimizedHorseDatabase)]:
            
            if impl_name == 'optimized':
                db = db_class(cache_size=500, enable_indexing=False)  # Smaller cache under pressure
            else:
                db = db_class()
            
            # Add data in chunks and monitor performance
            chunk_size = 10000
            performance_progression = []
            
            for i in range(0, len(large_horses), chunk_size):
                chunk = large_horses[i:i + chunk_size]
                
                start_time = time.time()
                if hasattr(db, 'add_horses_bulk'):
                    db.add_horses_bulk(chunk)
                else:
                    for horse_id, data in chunk:
                        db.add_horse(horse_id, data)
                
                chunk_time = time.time() - start_time
                
                # Test lookup performance after each chunk
                sample_ids = random.sample([h[0] for h in chunk], min(100, len(chunk)))
                lookup_start = time.time()
                for horse_id in sample_ids:
                    db.get_horse(horse_id)
                lookup_time = time.time() - lookup_start
                
                performance_progression.append({
                    'records': i + len(chunk),
                    'chunk_time': chunk_time,
                    'records_per_second': len(chunk) / chunk_time,
                    'avg_lookup_time': lookup_time / len(sample_ids)
                })
            
            memory_results[impl_name] = {
                'performance_progression': performance_progression,
                'avg_records_per_second': statistics.mean([p['records_per_second'] for p in performance_progression]),
                'final_lookup_time': performance_progression[-1]['avg_lookup_time']
            }
            
            # Cleanup
            del db
            gc.collect()
        
        return memory_results
    
    def _test_extreme_sizes(self) -> Dict[str, Any]:
        """Test with extreme dataset sizes."""
        print("🚀 Testing extreme sizes...")
        
        extreme_results = {}
        extreme_sizes = [100000, 250000]  # Reduced for memory constraints
        
        for size in extreme_sizes:
            print(f"Testing with {size:,} records...")
            
            try:
                start_time = time.time()
                horses, race_times = self.generate_large_dataset(size)
                generation_time = time.time() - start_time
                
                # Test only optimized implementations for extreme sizes
                db = OptimizedHorseDatabase(cache_size=min(5000, size // 100), enable_indexing=False)
                
                # Bulk insert test
                start_time = time.time()
                horses_data = [(h[0], h[1]) for h in horses]
                db.add_horses_bulk(horses_data)
                insert_time = time.time() - start_time
                
                # Sample operations test
                sample_ids = random.sample([h[0] for h in horses], min(1000, size // 100))
                
                start_time = time.time()
                for horse_id in sample_ids:
                    db.get_horse(horse_id)
                lookup_time = time.time() - start_time
                
                extreme_results[size] = {
                    'generation_time': generation_time,
                    'insert_time': insert_time,
                    'insert_rate': size / insert_time,
                    'lookup_time': lookup_time,
                    'lookup_rate': len(sample_ids) / lookup_time,
                    'memory_usage': db.get_memory_usage_estimate() if hasattr(db, 'get_memory_usage_estimate') else None
                }
                
                del db
                gc.collect()
                
            except MemoryError:
                extreme_results[size] = {'error': 'Memory limit exceeded'}
            except Exception as e:
                extreme_results[size] = {'error': str(e)}
        
        return extreme_results
    
    def _calculate_improvement(self, original: Dict, optimized: Dict) -> Dict[str, float]:
        """Calculate performance improvements."""
        improvements = {}
        
        # Compare common metrics
        metrics_to_compare = [
            ('bulk_insert_time', 'speedup'),
            ('avg_lookup_time', 'speedup'),
            ('avg_range_query_time', 'speedup'),
            ('insert_rate', 'improvement'),
            ('lookup_rate', 'improvement')
        ]
        
        for metric, improvement_type in metrics_to_compare:
            if metric in original and metric in optimized:
                orig_val = original[metric]
                opt_val = optimized[metric]
                
                # Skip None values
                if orig_val is not None and opt_val is not None and orig_val > 0:
                    if improvement_type == 'speedup':
                        improvements[f'{metric}_speedup'] = orig_val / opt_val if opt_val > 0 else float('inf')
                    else:
                        improvements[f'{metric}_improvement'] = ((opt_val - orig_val) / orig_val) * 100
        
        return improvements
    
    def generate_performance_report(self, results: Dict[str, Any], output_file: str = None) -> str:
        """Generate comprehensive performance report."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if output_file is None:
            output_file = f"performance_report_{timestamp}.json"
        
        # Add metadata
        report = {
            'timestamp': timestamp,
            'system_info': {
                'python_version': sys.version,
                'platform': sys.platform
            },
            'results': results
        }
        
        # Save to file
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        return output_file
    
    def print_performance_summary(self, scalability_results: Dict[str, Any]):
        """Print a detailed performance summary."""
        print("\\n" + "=" * 80)
        print("PERFORMANCE ANALYSIS SUMMARY")
        print("=" * 80)
        
        # Extract improvement data
        sizes = sorted(scalability_results.keys())
        
        print("\\n📊 SCALABILITY RESULTS")
        print("-" * 50)
        print(f"{'Size':<10} {'Hash Insert':<15} {'Hash Lookup':<15} {'Heap Insert':<15} {'Tree Range':<15}")
        print("-" * 75)
        
        for size in sizes:
            results = scalability_results[size]
            
            # Hash table improvements
            hash_insert_speedup = results['hash_table']['improvement'].get('bulk_insert_time_speedup', 1.0)
            hash_lookup_speedup = results['hash_table']['improvement'].get('avg_lookup_time_speedup', 1.0)
            
            # Leaderboard improvements  
            heap_insert_speedup = results['leaderboard']['improvement'].get('bulk_insert_time_speedup', 1.0)
            
            # AVL tree improvements
            tree_range_speedup = results['avl_tree']['improvement'].get('avg_range_query_time_speedup', 1.0)
            
            print(f"{size:<10} {hash_insert_speedup:<15.2f} {hash_lookup_speedup:<15.2f} "
                  f"{heap_insert_speedup:<15.2f} {tree_range_speedup:<15.2f}")
        
        # Cache performance analysis
        print("\\n🎯 CACHE PERFORMANCE")
        print("-" * 50)
        for size in sizes[-3:]:  # Show last 3 sizes
            cache_stats = scalability_results[size]['hash_table']['optimized'].get('cache_stats', {})
            hit_rate = cache_stats.get('hit_rate', 0)
            print(f"Size {size}: Cache hit rate = {hit_rate:.1f}%")
        
        # Memory efficiency
        print("\\n💾 MEMORY EFFICIENCY")
        print("-" * 50)
        for size in sizes[-2:]:  # Show last 2 sizes
            hash_memory = scalability_results[size]['hash_table']['optimized'].get('memory_breakdown', {})
            total_memory = hash_memory.get('total', 0) / 1024 / 1024  # Convert to MB
            print(f"Size {size}: Memory usage = {total_memory:.1f} MB")


def main():
    """Run comprehensive Phase 3 benchmarking suite."""
    print("🏁 PHASE 3: ADVANCED PERFORMANCE ANALYSIS 🏁")
    print("=" * 80)
    
    benchmark_suite = SimplifiedBenchmarkSuite()
    
    # Run scalability analysis
    print("\\n📊 Running Scalability Analysis...")
    scalability_results = benchmark_suite.run_scalability_analysis([1000, 5000, 10000, 25000])
    
    # Run stress tests
    print("\\n⚡ Running Stress Tests...")
    stress_results = benchmark_suite.run_stress_tests()
    
    # Combine all results
    all_results = {
        'scalability': scalability_results,
        'stress_tests': stress_results
    }
    
    # Generate report
    print("\\n📝 Generating Performance Report...")
    report_file = benchmark_suite.generate_performance_report(all_results)
    print(f"Report saved to: {report_file}")
    
    # Print summary
    benchmark_suite.print_performance_summary(scalability_results)
    
    print("\\n" + "=" * 80)
    print("PHASE 3 ANALYSIS COMPLETE")
    print("=" * 80)
    print("✅ Scalability analysis completed")
    print("✅ Stress testing completed")
    print("✅ Performance report generated")
    print("\\nOptimizations implemented:")
    print("• LRU caching with TTL")
    print("• Secondary indexing")
    print("• Bulk operations")
    print("• Memory pooling")
    print("• Range query optimization")
    print("• Concurrent access support")
    

if __name__ == "__main__":
    main()
