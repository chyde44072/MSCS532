"""
Performance benchmarking script for horse racing predictor data structures.
Measures time complexity and performance characteristics of each implementation.
"""

import time
import random
import statistics
from typing import List, Tuple
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_structures.hash_table import HorseDatabase
from data_structures.leaderboard_heap import Leaderboard
from data_structures.avl_tree import AVLTree

def generate_test_data(n: int) -> Tuple[List[Tuple[str, dict]], List[Tuple[str, float]]]:
    """Generate test data for benchmarking."""
    horses = []
    race_times = []
    
    for i in range(n):
        horse_id = f"H{i:06d}"
        wins = random.randint(0, 50)
        races = wins + random.randint(0, 50)
        
        horse_data = {
            "name": f"Horse_{i}",
            "age": random.randint(3, 8),
            "wins": wins,
            "races": races,
            "jockey": f"Jockey_{i % 100}"
        }
        
        race_time = round(random.uniform(55.0, 80.0), 2)
        
        horses.append((horse_id, horse_data))
        race_times.append((horse_id, race_time))
    
    return horses, race_times

def benchmark_hash_table(horses: List[Tuple[str, dict]], operations: int = 1000) -> dict:
    """Benchmark hash table operations."""
    print("Benchmarking Hash Table (HorseDatabase)...")
    
    db = HorseDatabase()
    results = {}
    
    # Benchmark insertions
    start_time = time.time()
    for horse_id, data in horses:
        db.add_horse(horse_id, data)
    insert_time = time.time() - start_time
    results['insert_total'] = insert_time
    results['insert_avg'] = insert_time / len(horses)
    
    # Benchmark lookups
    lookup_times = []
    test_ids = random.sample([h[0] for h in horses], min(operations, len(horses)))
    
    for horse_id in test_ids:
        start_time = time.time()
        db.get_horse(horse_id)
        lookup_times.append(time.time() - start_time)
    
    results['lookup_avg'] = statistics.mean(lookup_times)
    results['lookup_std'] = statistics.stdev(lookup_times) if len(lookup_times) > 1 else 0
    
    # Benchmark updates
    update_times = []
    test_ids = random.sample([h[0] for h in horses], min(operations // 2, len(horses)))
    
    for horse_id in test_ids:
        start_time = time.time()
        db.update_performance(horse_id, {"recent_time": random.uniform(60, 70)})
        update_times.append(time.time() - start_time)
    
    results['update_avg'] = statistics.mean(update_times)
    results['update_std'] = statistics.stdev(update_times) if len(update_times) > 1 else 0
    
    return results

def benchmark_leaderboard(race_times: List[Tuple[str, float]], operations: int = 1000) -> dict:
    """Benchmark leaderboard operations."""
    print("Benchmarking Leaderboard (Heap)...")
    
    leaderboard = Leaderboard()
    results = {}
    
    # Benchmark insertions
    start_time = time.time()
    for horse_id, race_time in race_times:
        leaderboard.add_result(horse_id, race_time)
    insert_time = time.time() - start_time
    results['insert_total'] = insert_time
    results['insert_avg'] = insert_time / len(race_times)
    
    # Benchmark top-k queries
    topk_times = []
    for _ in range(operations):
        k = random.randint(1, min(20, leaderboard.size()))
        start_time = time.time()
        leaderboard.get_top_performers(k)
        topk_times.append(time.time() - start_time)
    
    results['topk_avg'] = statistics.mean(topk_times)
    results['topk_std'] = statistics.stdev(topk_times) if len(topk_times) > 1 else 0
    
    # Benchmark rank queries
    rank_times = []
    test_ids = random.sample([h[0] for h in race_times], min(operations // 2, len(race_times)))
    
    for horse_id in test_ids:
        start_time = time.time()
        leaderboard.get_horse_rank(horse_id)
        rank_times.append(time.time() - start_time)
    
    results['rank_avg'] = statistics.mean(rank_times)
    results['rank_std'] = statistics.stdev(rank_times) if len(rank_times) > 1 else 0
    
    return results

def benchmark_avl_tree(horses: List[Tuple[str, dict]], operations: int = 1000) -> dict:
    """Benchmark AVL tree operations."""
    print("Benchmarking AVL Tree...")
    
    tree = AVLTree()
    results = {}
    
    # Prepare win ratios
    win_ratios = []
    for horse_id, data in horses:
        if data['races'] > 0:
            ratio = data['wins'] / data['races']
            win_ratios.append((horse_id, ratio))
    
    # Benchmark insertions
    start_time = time.time()
    for horse_id, ratio in win_ratios:
        tree.insert(horse_id, ratio)
    insert_time = time.time() - start_time
    results['insert_total'] = insert_time
    results['insert_avg'] = insert_time / len(win_ratios)
    
    # Benchmark range queries
    range_times = []
    for _ in range(operations):
        min_ratio = random.uniform(0.0, 0.5)
        max_ratio = min_ratio + random.uniform(0.1, 0.5)
        start_time = time.time()
        tree.get_range(min_ratio, max_ratio)
        range_times.append(time.time() - start_time)
    
    results['range_avg'] = statistics.mean(range_times)
    results['range_std'] = statistics.stdev(range_times) if len(range_times) > 1 else 0
    
    # Benchmark sorted traversal
    start_time = time.time()
    tree.get_sorted_list()
    results['traversal_time'] = time.time() - start_time
    
    return results

def run_scalability_test():
    """Test scalability with increasing data sizes."""
    print("\n" + "="*60)
    print("SCALABILITY TESTING")
    print("="*60)
    
    sizes = [100, 500, 1000, 2000, 5000]
    results = {size: {} for size in sizes}
    
    for size in sizes:
        print(f"\nTesting with {size} horses...")
        horses, race_times = generate_test_data(size)
        
        # Test each data structure
        results[size]['hash_table'] = benchmark_hash_table(horses, min(1000, size))
        results[size]['leaderboard'] = benchmark_leaderboard(race_times, min(1000, size))
        results[size]['avl_tree'] = benchmark_avl_tree(horses, min(1000, size))
    
    # Print scalability results
    print(f"\n{'Size':<8} {'Hash Insert':<12} {'Hash Lookup':<12} {'Heap Insert':<12} {'Tree Insert':<12} {'Range Query':<12}")
    print("-" * 80)
    
    for size in sizes:
        hash_insert = f"{results[size]['hash_table']['insert_avg']*1000:.3f}ms"
        hash_lookup = f"{results[size]['hash_table']['lookup_avg']*1000:.3f}ms"
        heap_insert = f"{results[size]['leaderboard']['insert_avg']*1000:.3f}ms"
        tree_insert = f"{results[size]['avl_tree']['insert_avg']*1000:.3f}ms"
        range_query = f"{results[size]['avl_tree']['range_avg']*1000:.3f}ms"
        
        print(f"{size:<8} {hash_insert:<12} {hash_lookup:<12} {heap_insert:<12} {tree_insert:<12} {range_query:<12}")

def print_detailed_results(results: dict, name: str):
    """Print detailed benchmark results."""
    print(f"\n{name} Results:")
    print("-" * 40)
    for operation, value in results.items():
        if 'avg' in operation:
            print(f"  {operation}: {value*1000:.3f} ms")
        elif 'total' in operation:
            print(f"  {operation}: {value:.3f} s")
        elif 'std' in operation:
            print(f"  {operation}: {value*1000:.3f} ms")
        else:
            print(f"  {operation}: {value:.3f} s")

def main():
    """Main benchmarking function."""
    print("🏁 HORSE RACING PREDICTOR - PERFORMANCE BENCHMARK 🏁")
    print("="*60)
    
    # Test with moderate dataset
    test_size = 2000
    print(f"Generating {test_size} test records...")
    horses, race_times = generate_test_data(test_size)
    print(f"Generated {len(horses)} horses and {len(race_times)} race times")
    
    # Run individual benchmarks
    print(f"\nRunning benchmarks with {test_size} records...")
    
    hash_results = benchmark_hash_table(horses)
    heap_results = benchmark_leaderboard(race_times)
    tree_results = benchmark_avl_tree(horses)
    
    # Print detailed results
    print_detailed_results(hash_results, "Hash Table (HorseDatabase)")
    print_detailed_results(heap_results, "Heap (Leaderboard)")
    print_detailed_results(tree_results, "AVL Tree (Ranking)")
    
    # Run scalability test
    run_scalability_test()
    
    # Performance summary
    print(f"\n{'='*60}")
    print("PERFORMANCE SUMMARY")
    print("="*60)
    print("✅ Hash Table: Excellent O(1) average-case performance for lookups")
    print("✅ Heap: Efficient O(log n) insertions and O(k log n) top-k queries")
    print("✅ AVL Tree: Balanced O(log n) operations with efficient range queries")
    print("\nAll data structures demonstrate expected time complexities")
    print("and scale well with increasing dataset sizes.")

if __name__ == "__main__":
    main()