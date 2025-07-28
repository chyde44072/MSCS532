"""
This module provides thorough testing for all implemented algorithms and
data structures to ensure correctness, robustness, and performance validation.
"""

import unittest
import random
from typing import List
import sys
import os

# Import our implementations
from selection_algorithms import SelectionAlgorithms
from data_structures import (
    SimpleStack, SimpleQueue, SimpleLinkedList, SimpleTree
)


class TestSelectionAlgorithms(unittest.TestCase):
    """Test cases for selection algorithms."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.selector = SelectionAlgorithms()
        random.seed(42)  # For reproducible tests
    
    def test_deterministic_selection_basic(self):
        """Test deterministic selection with basic cases."""
        # Simple case
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        result = self.selector.find_kth_smallest_deterministic(arr, 4)
        expected = sorted(arr)[3]  # 4th smallest (0-indexed: 3)
        self.assertEqual(result, expected)
        
        # Single element
        arr = [42]
        result = self.selector.find_kth_smallest_deterministic(arr, 1)
        self.assertEqual(result, 42)
        
        # Two elements
        arr = [5, 3]
        result = self.selector.find_kth_smallest_deterministic(arr, 1)
        self.assertEqual(result, 3)
        result = self.selector.find_kth_smallest_deterministic(arr, 2)
        self.assertEqual(result, 5)
    
    def test_randomized_selection_basic(self):
        """Test randomized selection with basic cases."""
        # Simple case
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        result = self.selector.find_kth_smallest_randomized(arr, 4)
        expected = sorted(arr)[3]
        self.assertEqual(result, expected)
        
        # Single element
        arr = [42]
        result = self.selector.find_kth_smallest_randomized(arr, 1)
        self.assertEqual(result, 42)
    
    def test_selection_with_duplicates(self):
        """Test selection algorithms with duplicate elements."""
        arr = [5, 5, 5, 5, 5]
        
        # All elements are the same
        for k in range(1, 6):
            det_result = self.selector.find_kth_smallest_deterministic(arr, k)
            rand_result = self.selector.find_kth_smallest_randomized(arr, k)
            self.assertEqual(det_result, 5)
            self.assertEqual(rand_result, 5)
        
        # Mixed duplicates
        arr = [1, 1, 2, 2, 3, 3]
        det_result = self.selector.find_kth_smallest_deterministic(arr, 3)
        rand_result = self.selector.find_kth_smallest_randomized(arr, 3)
        self.assertEqual(det_result, 2)
        self.assertEqual(rand_result, 2)
    
    def test_selection_edge_cases(self):
        """Test selection algorithms with edge cases."""
        # Test invalid inputs
        with self.assertRaises(ValueError):
            self.selector.find_kth_smallest_deterministic([], 1)
        
        with self.assertRaises(ValueError):
            self.selector.find_kth_smallest_deterministic([1, 2, 3], 0)
        
        with self.assertRaises(ValueError):
            self.selector.find_kth_smallest_deterministic([1, 2, 3], 4)
    
    def test_selection_consistency(self):
        """Test that both algorithms give same results."""
        test_cases = [
            [1, 2, 3, 4, 5],  # Sorted
            [5, 4, 3, 2, 1],  # Reverse sorted
            [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5],  # Random with duplicates
            list(range(1, 101)),  # Larger sorted array
        ]
        
        for arr in test_cases:
            for k in range(1, min(len(arr) + 1, 6)):  # Test first 5 positions
                det_result = self.selector.find_kth_smallest_deterministic(arr.copy(), k)
                rand_result = self.selector.find_kth_smallest_randomized(arr.copy(), k)
                expected = sorted(arr)[k-1]
                
                self.assertEqual(det_result, expected, 
                               f"Deterministic failed for k={k}, arr={arr}")
                self.assertEqual(rand_result, expected, 
                               f"Randomized failed for k={k}, arr={arr}")


class TestSimpleStack(unittest.TestCase):
    """Test cases for simple stack."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.stack = SimpleStack()
    
    def test_basic_operations(self):
        """Test basic stack operations."""
        # Test push and peek
        self.stack.push(1)
        self.stack.push(2)
        self.stack.push(3)
        self.assertEqual(self.stack.peek(), 3)
        self.assertEqual(self.stack.size(), 3)
        
        # Test pop
        self.assertEqual(self.stack.pop(), 3)
        self.assertEqual(self.stack.pop(), 2)
        self.assertEqual(self.stack.size(), 1)
        self.assertEqual(self.stack.peek(), 1)
        
        # Test pop last element
        self.assertEqual(self.stack.pop(), 1)
        self.assertTrue(self.stack.is_empty())
    
    def test_edge_cases(self):
        """Test stack edge cases."""
        # Test empty stack
        self.assertTrue(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 0)
        
        with self.assertRaises(IndexError):
            self.stack.pop()
        
        with self.assertRaises(IndexError):
            self.stack.peek()


class TestSimpleQueue(unittest.TestCase):
    """Test cases for simple queue."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.queue = SimpleQueue()
    
    def test_basic_operations(self):
        """Test basic queue operations."""
        # Test enqueue and peek
        self.queue.enqueue(1)
        self.queue.enqueue(2)
        self.queue.enqueue(3)
        self.assertEqual(self.queue.peek(), 1)
        self.assertEqual(self.queue.size(), 3)
        
        # Test dequeue
        self.assertEqual(self.queue.dequeue(), 1)
        self.assertEqual(self.queue.dequeue(), 2)
        self.assertEqual(self.queue.size(), 1)
        self.assertEqual(self.queue.peek(), 3)
        
        # Test dequeue last element
        self.assertEqual(self.queue.dequeue(), 3)
        self.assertTrue(self.queue.is_empty())
    
    def test_edge_cases(self):
        """Test queue edge cases."""
        # Test empty queue
        self.assertTrue(self.queue.is_empty())
        self.assertEqual(self.queue.size(), 0)
        
        with self.assertRaises(IndexError):
            self.queue.dequeue()
        
        with self.assertRaises(IndexError):
            self.queue.peek()


class TestSimpleLinkedList(unittest.TestCase):
    """Test cases for simple linked list."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ll = SimpleLinkedList()
    
    def test_insertion_operations(self):
        """Test insertion operations."""
        # Test insert at front
        self.ll.insert_front(1)
        self.ll.insert_front(2)
        self.assertEqual(self.ll.to_list(), [2, 1])
        
        # Test insert at back
        self.ll.insert_back(3)
        self.ll.insert_back(4)
        self.assertEqual(self.ll.to_list(), [2, 1, 3, 4])
    
    def test_deletion_operations(self):
        """Test deletion operations."""
        # Set up list
        for i in [1, 2, 3, 4, 5]:
            self.ll.insert_back(i)
        
        # Test delete at front
        deleted = self.ll.delete_front()
        self.assertEqual(deleted, 1)
        self.assertEqual(self.ll.to_list(), [2, 3, 4, 5])
    
    def test_search_operation(self):
        """Test search operation."""
        for i in [10, 20, 30]:
            self.ll.insert_back(i)
        
        self.assertEqual(self.ll.search(20), 1)
        self.assertEqual(self.ll.search(40), -1)
    
    def test_edge_cases(self):
        """Test edge cases."""
        # Test operations on empty list
        with self.assertRaises(IndexError):
            self.ll.delete_front()


class TestSimpleTree(unittest.TestCase):
    """Test cases for simple tree."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tree = SimpleTree("root")
    
    def test_tree_construction(self):
        """Test tree construction and basic operations."""
        # Add children
        self.assertTrue(self.tree.add_child("root", "A"))
        self.assertTrue(self.tree.add_child("root", "B"))
        self.assertTrue(self.tree.add_child("A", "C"))
        self.assertTrue(self.tree.add_child("A", "D"))
        
        self.assertEqual(len(self.tree), 5)
        
        # Test invalid parent
        self.assertFalse(self.tree.add_child("nonexistent", "E"))
    
    def test_tree_traversals(self):
        """Test tree traversal operations."""
        # Build tree: root -> [A, B], A -> [C, D]
        self.tree.add_child("root", "A")
        self.tree.add_child("root", "B")
        self.tree.add_child("A", "C")
        self.tree.add_child("A", "D")
        
        preorder = self.tree.preorder()
        self.assertEqual(preorder, ["root", "A", "C", "D", "B"])


class TestRunner:
    """Custom test runner with detailed reporting."""
    
    def __init__(self):
        self.test_results = {}
    
    def run_all_tests(self):
        """Run all test suites and generate report."""
        print("MSCS 532 - Assignment 6: Comprehensive Test Suite")
        print("=" * 70)
        
        test_classes = [
            TestSelectionAlgorithms,
            TestSimpleStack,
            TestSimpleQueue,
            TestSimpleLinkedList,
            TestSimpleTree
        ]
        
        total_tests = 0
        total_failures = 0
        total_errors = 0
        
        for test_class in test_classes:
            print(f"\nRunning {test_class.__name__}...")
            print("-" * 50)
            
            suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
            runner = unittest.TextTestRunner(verbosity=2)
            result = runner.run(suite)
            
            tests_run = result.testsRun
            failures = len(result.failures)
            errors = len(result.errors)
            
            total_tests += tests_run
            total_failures += failures
            total_errors += errors
            
            self.test_results[test_class.__name__] = {
                'tests_run': tests_run,
                'failures': failures,
                'errors': errors,
                'success_rate': (tests_run - failures - errors) / tests_run * 100
            }
            
            print(f"Tests run: {tests_run}, Failures: {failures}, Errors: {errors}")
        
        self.print_summary_report(total_tests, total_failures, total_errors)
    
    def print_summary_report(self, total_tests: int, total_failures: int, total_errors: int):
        """Print comprehensive test summary."""
        print("\n" + "=" * 70)
        print("TEST SUMMARY REPORT")
        print("=" * 70)
        
        success_rate = (total_tests - total_failures - total_errors) / total_tests * 100
        
        print(f"Total Tests Run: {total_tests}")
        print(f"Total Failures: {total_failures}")
        print(f"Total Errors: {total_errors}")
        print(f"Overall Success Rate: {success_rate:.1f}%")
        
        print("\nDetailed Results by Test Suite:")
        print("-" * 40)
        
        for suite_name, results in self.test_results.items():
            print(f"{suite_name:25} | {results['success_rate']:6.1f}% | "
                  f"{results['tests_run']:2d} tests")
        
        if total_failures == 0 and total_errors == 0:
            print("\n🎉 ALL TESTS PASSED! The implementation is working correctly.")
        else:
            print(f"\n⚠️  {total_failures + total_errors} test(s) failed. Please review the implementation.")
        
        print("\nTest Coverage Summary:")
        print("✓ Selection Algorithms: Deterministic and Randomized")
        print("✓ Data Structures: Simple Stack, Queue, Linked List, Tree")
        print("✓ Edge Cases: Empty inputs, boundary conditions, error handling")
        print("✓ Consistency: Algorithm correctness across different input types")


def main():
    """Main function to run all tests."""
    runner = TestRunner()
    runner.run_all_tests()


if __name__ == "__main__":
    main()
