import unittest
import random
from quicksort import QuickSort


class TestQuickSort(unittest.TestCase):
    """Test cases for QuickSort implementations."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.quicksort = QuickSort()
    
    def test_empty_array(self):
        """Test sorting an empty array."""
        arr = []
        
        # Test deterministic version
        result_det = self.quicksort.deterministic_quicksort(arr.copy())
        self.assertEqual(result_det, [])
        
        # Test randomized version
        result_rand = self.quicksort.randomized_quicksort(arr.copy())
        self.assertEqual(result_rand, [])
    
    def test_single_element(self):
        """Test sorting a single-element array."""
        arr = [42]
        
        # Test deterministic version
        result_det = self.quicksort.deterministic_quicksort(arr.copy())
        self.assertEqual(result_det, [42])
        
        # Test randomized version
        result_rand = self.quicksort.randomized_quicksort(arr.copy())
        self.assertEqual(result_rand, [42])
    
    def test_two_elements(self):
        """Test sorting a two-element array."""
        # Test case 1: already sorted
        arr1 = [1, 2]
        result_det1 = self.quicksort.deterministic_quicksort(arr1.copy())
        result_rand1 = self.quicksort.randomized_quicksort(arr1.copy())
        self.assertEqual(result_det1, [1, 2])
        self.assertEqual(result_rand1, [1, 2])
        
        # Test case 2: reverse sorted
        arr2 = [2, 1]
        result_det2 = self.quicksort.deterministic_quicksort(arr2.copy())
        result_rand2 = self.quicksort.randomized_quicksort(arr2.copy())
        self.assertEqual(result_det2, [1, 2])
        self.assertEqual(result_rand2, [1, 2])
    
    def test_already_sorted(self):
        """Test sorting an already sorted array."""
        arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        expected = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        # Test deterministic version
        result_det = self.quicksort.deterministic_quicksort(arr.copy())
        self.assertEqual(result_det, expected)
        
        # Test randomized version
        result_rand = self.quicksort.randomized_quicksort(arr.copy())
        self.assertEqual(result_rand, expected)
    
    def test_reverse_sorted(self):
        """Test sorting a reverse sorted array."""
        arr = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        expected = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        # Test deterministic version
        result_det = self.quicksort.deterministic_quicksort(arr.copy())
        self.assertEqual(result_det, expected)
        
        # Test randomized version
        result_rand = self.quicksort.randomized_quicksort(arr.copy())
        self.assertEqual(result_rand, expected)
    
    def test_random_array(self):
        """Test sorting a random array."""
        arr = [64, 34, 25, 12, 22, 11, 90, 88, 76, 50, 42]
        expected = sorted(arr)
        
        # Test deterministic version
        result_det = self.quicksort.deterministic_quicksort(arr.copy())
        self.assertEqual(result_det, expected)
        
        # Test randomized version
        result_rand = self.quicksort.randomized_quicksort(arr.copy())
        self.assertEqual(result_rand, expected)
    
    def test_duplicates(self):
        """Test sorting an array with duplicate elements."""
        arr = [5, 2, 8, 2, 9, 1, 5, 5, 2, 8]
        expected = sorted(arr)
        
        # Test deterministic version
        result_det = self.quicksort.deterministic_quicksort(arr.copy())
        self.assertEqual(result_det, expected)
        
        # Test randomized version
        result_rand = self.quicksort.randomized_quicksort(arr.copy())
        self.assertEqual(result_rand, expected)
    
    def test_all_same_elements(self):
        """Test sorting an array where all elements are the same."""
        arr = [7, 7, 7, 7, 7, 7, 7]
        expected = [7, 7, 7, 7, 7, 7, 7]
        
        # Test deterministic version
        result_det = self.quicksort.deterministic_quicksort(arr.copy())
        self.assertEqual(result_det, expected)
        
        # Test randomized version
        result_rand = self.quicksort.randomized_quicksort(arr.copy())
        self.assertEqual(result_rand, expected)
    
    def test_negative_numbers(self):
        """Test sorting an array with negative numbers."""
        arr = [-5, 3, -2, 8, -10, 0, 15, -3]
        expected = sorted(arr)
        
        # Test deterministic version
        result_det = self.quicksort.deterministic_quicksort(arr.copy())
        self.assertEqual(result_det, expected)
        
        # Test randomized version
        result_rand = self.quicksort.randomized_quicksort(arr.copy())
        self.assertEqual(result_rand, expected)
    
    def test_large_random_array(self):
        """Test sorting a large random array."""
        random.seed(42)  # For reproducible results
        arr = [random.randint(-1000, 1000) for _ in range(100)]
        expected = sorted(arr)
        
        # Test deterministic version
        result_det = self.quicksort.deterministic_quicksort(arr.copy())
        self.assertEqual(result_det, expected)
        
        # Test randomized version
        result_rand = self.quicksort.randomized_quicksort(arr.copy())
        self.assertEqual(result_rand, expected)
    
    def test_performance_counters(self):
        """Test that performance counters are working correctly."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6, 5]
        
        # Test deterministic version
        self.quicksort.deterministic_quicksort(arr.copy())
        stats_det = self.quicksort.get_performance_stats()
        
        # Verify that counters are positive for non-trivial input
        self.assertGreater(stats_det['comparisons'], 0)
        self.assertGreater(stats_det['recursive_calls'], 0)
        self.assertGreaterEqual(stats_det['swaps'], 0)  # Swaps can be 0 for sorted input
        
        # Test randomized version
        self.quicksort.randomized_quicksort(arr.copy())
        stats_rand = self.quicksort.get_performance_stats()
        
        # Verify that counters are positive for non-trivial input
        self.assertGreater(stats_rand['comparisons'], 0)
        self.assertGreater(stats_rand['recursive_calls'], 0)
        self.assertGreaterEqual(stats_rand['swaps'], 0)
    
    def test_algorithm_consistency(self):
        """Test that both algorithms produce the same result for multiple runs."""
        test_cases = [
            [64, 34, 25, 12, 22, 11, 90],
            [5, 5, 5, 5],
            [1],
            [],
            [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
            [-5, 0, 3, -2, 8]
        ]
        
        for arr in test_cases:
            expected = sorted(arr)
            
            # Test multiple runs of deterministic version
            for _ in range(3):
                result_det = self.quicksort.deterministic_quicksort(arr.copy())
                self.assertEqual(result_det, expected, 
                               f"Deterministic failed for {arr}")
            
            # Test multiple runs of randomized version
            for _ in range(3):
                result_rand = self.quicksort.randomized_quicksort(arr.copy())
                self.assertEqual(result_rand, expected, 
                               f"Randomized failed for {arr}")


class TestQuickSortEdgeCases(unittest.TestCase):
    """Test edge cases and special scenarios."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.quicksort = QuickSort()
    
    def test_worst_case_deterministic(self):
        """Test worst-case scenario for deterministic quicksort."""
        # Worst case: already sorted array (pivot is always the largest)
        arr = list(range(1, 21))  # [1, 2, 3, ..., 20]
        expected = arr.copy()
        
        result = self.quicksort.deterministic_quicksort(arr.copy())
        self.assertEqual(result, expected)
        
        # Check that many recursive calls were made (indicating worst case)
        stats = self.quicksort.get_performance_stats()
        self.assertGreaterEqual(stats['recursive_calls'], len(arr) - 1)
    
    def test_best_case_scenario(self):
        """Test best-case scenario where pivot always divides array in half."""
        # Create an array where the last element is median
        arr = [1, 3, 2, 5, 4, 7, 6, 9, 8]  # Last element is often median
        expected = sorted(arr)
        
        result = self.quicksort.deterministic_quicksort(arr.copy())
        self.assertEqual(result, expected)
    
    def test_random_vs_deterministic_comparison(self):
        """Compare randomized vs deterministic on problematic inputs."""
        # Test on reverse sorted array (worst case for deterministic)
        arr = list(range(50, 0, -1))  # [50, 49, 48, ..., 1]
        expected = sorted(arr)
        
        # Test deterministic version
        result_det = self.quicksort.deterministic_quicksort(arr.copy())
        stats_det = self.quicksort.get_performance_stats()
        
        # Test randomized version
        result_rand = self.quicksort.randomized_quicksort(arr.copy())
        stats_rand = self.quicksort.get_performance_stats()
        
        # Both should produce correct results
        self.assertEqual(result_det, expected)
        self.assertEqual(result_rand, expected)
        
        # Randomized version should typically use fewer recursive calls
        # (though this is probabilistic, so we don't enforce it strictly)
        print(f"Deterministic recursive calls: {stats_det['recursive_calls']}")
        print(f"Randomized recursive calls: {stats_rand['recursive_calls']}")


def run_comprehensive_tests():
    """Run all test suites and provide detailed output."""
    print("="*60)
    print("QUICKSORT ALGORITHM TEST SUITE")
    print("="*60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestQuickSort))
    suite.addTests(loader.loadTestsFromTestCase(TestQuickSortEdgeCases))
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n✅ All tests passed successfully!")
        print("Both deterministic and randomized Quicksort implementations are working correctly.")
    else:
        print("\n❌ Some tests failed. Please review the implementation.")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_comprehensive_tests()
