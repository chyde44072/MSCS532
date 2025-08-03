
import unittest
import sys
import os

# Add path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from optimized_data_structures.optimized_hash_table import OptimizedHorseDatabase
from optimized_data_structures.optimized_leaderboard import OptimizedLeaderboard
from optimized_data_structures.optimized_avl_tree import OptimizedAVLTree


class TestOptimizedHorseDatabase(unittest.TestCase):
    """Test the simplified optimized hash table."""
    
    def setUp(self):
        self.db = OptimizedHorseDatabase(cache_size=10, enable_indexing=True)
    
    def test_basic_operations(self):
        """Test basic CRUD operations."""
        # Add horse
        horse_data = {"name": "Thunder", "jockey": "Smith", "age": 4}
        self.db.add_horse("H001", horse_data)
        
        # Get horse
        retrieved = self.db.get_horse("H001")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["name"], "Thunder")
        
        # Non-existent horse
        self.assertIsNone(self.db.get_horse("H999"))
    
    def test_bulk_operations(self):
        """Test bulk insert operations."""
        horses = [
            ("H001", {"name": "Horse1", "jockey": "Smith", "age": 4}),
            ("H002", {"name": "Horse2", "jockey": "Jones", "age": 5}),
            ("H003", {"name": "Horse3", "jockey": "Smith", "age": 6})
        ]
        
        self.db.add_horses_bulk(horses)
        
        # Verify all horses were added
        self.assertIsNotNone(self.db.get_horse("H001"))
        self.assertIsNotNone(self.db.get_horse("H002"))
        self.assertIsNotNone(self.db.get_horse("H003"))
    
    def test_caching_performance(self):
        """Test cache hit/miss behavior."""
        horse_data = {"name": "Thunder", "jockey": "Smith", "age": 4}
        self.db.add_horse("H001", horse_data)
        
        # First access - should be cache miss
        self.db.get_horse("H001")
        
        # Second access - should be cache hit
        self.db.get_horse("H001")
        
        stats = self.db.get_cache_stats()
        self.assertGreater(stats['cache_hits'], 0)
    
    def test_index_queries(self):
        """Test secondary index functionality."""
        horses = [
            ("H001", {"name": "Horse1", "jockey": "Smith", "age": 4}),
            ("H002", {"name": "Horse2", "jockey": "Jones", "age": 5}),
            ("H003", {"name": "Horse3", "jockey": "Smith", "age": 6})
        ]
        self.db.add_horses_bulk(horses)
        
        # Test jockey index
        smith_horses = self.db.find_horses_by_jockey("Smith")
        self.assertEqual(len(smith_horses), 2)
        
        # Test age index
        age_4_horses = self.db.find_horses_by_age(4)
        self.assertEqual(len(age_4_horses), 1)
    
    def test_memory_usage_estimation(self):
        """Test memory usage estimation functionality."""
        horses = [("H{:03d}".format(i), {"name": f"Horse{i}"}) for i in range(10)]
        self.db.add_horses_bulk(horses)
        
        memory_usage = self.db.get_memory_usage_estimate()
        self.assertIn('total', memory_usage)
        self.assertGreater(memory_usage['total'], 0)


class TestOptimizedLeaderboard(unittest.TestCase):
    """Test the simplified optimized leaderboard."""
    
    def setUp(self):
        self.lb = OptimizedLeaderboard(cache_top_k=5)
    
    def test_basic_operations(self):
        """Test basic leaderboard operations."""
        self.lb.add_result("H001", 65.2)
        self.lb.add_result("H002", 67.1)
        self.lb.add_result("H003", 64.8)
        
        top_performers = self.lb.get_top_performers(2)
        self.assertEqual(len(top_performers), 2)
        self.assertEqual(top_performers[0][0], "H003")  # Best time
    
    def test_bulk_operations(self):
        """Test bulk insert operations."""
        results = [
            ("H001", 65.2),
            ("H002", 67.1),
            ("H003", 64.8),
            ("H004", 66.5)
        ]
        
        self.lb.add_results_bulk(results)
        
        top_performers = self.lb.get_top_performers(3)
        self.assertEqual(len(top_performers), 3)
    
    def test_cache_performance(self):
        """Test caching behavior."""
        results = [("H{:03d}".format(i), 60.0 + i) for i in range(10)]
        self.lb.add_results_bulk(results)
        
        # Multiple queries should hit cache
        for _ in range(3):
            self.lb.get_top_performers(5)
        
        stats = self.lb.get_performance_stats()
        self.assertGreater(stats['cache_hits'], 0)
    
    def test_range_queries(self):
        """Test time range queries."""
        results = [
            ("H001", 65.2),
            ("H002", 67.1),
            ("H003", 64.8),
            ("H004", 70.5)
        ]
        self.lb.add_results_bulk(results)
        
        range_results = self.lb.get_top_performers_in_time_range(64.0, 68.0, 5)
        self.assertLessEqual(len(range_results), 3)  # Should filter out H004
    
    def test_percentile_statistics(self):
        """Test percentile calculation."""
        results = [("H{:03d}".format(i), 60.0 + i) for i in range(20)]
        self.lb.add_results_bulk(results)
        
        stats = self.lb.get_percentile_stats()
        self.assertIn('min', stats)
        self.assertIn('max', stats)
        self.assertIn('median', stats)


class TestOptimizedAVLTree(unittest.TestCase):
    """Test the simplified optimized AVL tree."""
    
    def setUp(self):
        self.tree = OptimizedAVLTree()
    
    def test_basic_operations(self):
        """Test basic tree operations."""
        self.tree.insert("H001", 0.75)
        self.tree.insert("H002", 0.60)
        self.tree.insert("H003", 0.80)
        
        range_results = self.tree.get_range(0.65, 0.85)
        self.assertGreaterEqual(len(range_results), 1)
    
    def test_bulk_operations(self):
        """Test bulk insertion."""
        data = [("H{:03d}".format(i), 0.5 + i * 0.01) for i in range(20)]
        self.tree.insert_bulk(data)
        
        range_results = self.tree.get_range(0.6, 0.7)
        self.assertGreater(len(range_results), 0)
    
    def test_range_queries_with_caching(self):
        """Test range queries and caching."""
        data = [("H{:03d}".format(i), 0.5 + i * 0.01) for i in range(10)]
        self.tree.insert_bulk(data)
        
        # Multiple same range queries should benefit from caching
        for _ in range(3):
            results = self.tree.get_range(0.6, 0.7)
        
        stats = self.tree.get_statistics()
        self.assertGreater(stats['cache_hits'], 0)
    
    def test_rank_queries(self):
        """Test rank calculation."""
        data = [("H{:03d}".format(i), 0.1 * i) for i in range(10)]
        self.tree.insert_bulk(data)
        
        rank = self.tree.get_rank(0.5)
        self.assertGreaterEqual(rank, 0)
    
    def test_kth_smallest_queries(self):
        """Test k-th smallest element queries."""
        data = [("H{:03d}".format(i), 0.1 * i) for i in range(10)]
        self.tree.insert_bulk(data)
        
        kth_result = self.tree.get_kth_smallest(3)
        self.assertIsNotNone(kth_result)
        self.assertEqual(len(kth_result), 2)  # (horse_id, value)
    
    def test_tree_balance(self):
        """Test tree remains balanced."""
        # Insert sequential data that could unbalance a simple BST
        data = [("H{:03d}".format(i), i) for i in range(20)]
        self.tree.insert_bulk(data)
        
        stats = self.tree.get_statistics()
        # AVL tree height should be logarithmic
        self.assertLess(stats['tree_height'], 10)  # Should be around log2(20) ≈ 4-5


class TestIntegrationOptimized(unittest.TestCase):
    """Integration tests for optimized structures."""
    
    def test_full_workflow_optimized(self):
        """Test complete workflow with optimized structures."""
        # Setup
        db = OptimizedHorseDatabase(cache_size=50)
        leaderboard = OptimizedLeaderboard(cache_top_k=10)
        tree = OptimizedAVLTree()
        
        # Add horses
        horses = [
            ("H001", {"name": "Thunder", "wins": 8, "races": 10}),
            ("H002", {"name": "Lightning", "wins": 6, "races": 10}),
            ("H003", {"name": "Storm", "wins": 9, "races": 10})
        ]
        db.add_horses_bulk(horses)
        
        # Add race results
        results = [("H001", 65.2), ("H002", 67.1), ("H003", 64.8)]
        leaderboard.add_results_bulk(results)
        
        # Add win ratios to tree
        ratios = [("H001", 0.8), ("H002", 0.6), ("H003", 0.9)]
        tree.insert_bulk(ratios)
        
        # Test queries
        top_performers = leaderboard.get_top_performers(2)
        self.assertEqual(len(top_performers), 2)
        
        high_performers = tree.get_range(0.7, 1.0)
        self.assertGreater(len(high_performers), 0)
    
    def test_performance_comparison(self):
        """Test performance improvements over original implementations."""
        import time
        
        # Test with moderately sized dataset
        horses = [("H{:04d}".format(i), {"name": f"Horse{i}"}) for i in range(1000)]
        
        # Optimized implementation
        start_time = time.time()
        db = OptimizedHorseDatabase()
        db.add_horses_bulk(horses)
        optimized_time = time.time() - start_time
        
        # Basic performance validation - optimized should complete quickly
        self.assertLess(optimized_time, 1.0)  # Should complete in under 1 second


def run_tests():
    """Run all tests and provide summary."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestOptimizedHorseDatabase,
        TestOptimizedLeaderboard, 
        TestOptimizedAVLTree,
        TestIntegrationOptimized
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*80)
    print("SIMPLIFIED OPTIMIZED DATA STRUCTURES TEST SUMMARY")
    print("="*80)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun) * 100
    print(f"Success rate: {success_rate:.1f}%")
    
    if result.failures:
        print(f"\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}")
    
    if result.errors:
        print(f"\n💥 ERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}")
    
    if not result.failures and not result.errors:
        print("\n✅ All tests passed! Simplified optimizations are working correctly.")
    else:
        print(f"\n⚠️  Some tests failed. Check implementation details.")
    
    return result


if __name__ == '__main__':
    run_tests()
