"""
Comprehensive test suite for horse racing predictor data structures.
Tests cover normal operations, edge cases, and error conditions.
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_structures.hash_table import HorseDatabase
from data_structures.leaderboard_heap import Leaderboard
from data_structures.avl_tree import AVLTree

class TestHorseDatabase(unittest.TestCase):
    """Test cases for HorseDatabase (Hash Table implementation)."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.db = HorseDatabase()
        self.sample_data = {
            "name": "Test Horse",
            "age": 4,
            "wins": 5,
            "races": 10,
            "jockey": "Test Jockey"
        }

    def test_add_and_get_horse(self):
        """Test adding and retrieving horse data."""
        self.db.add_horse("H001", self.sample_data)
        retrieved = self.db.get_horse("H001")
        self.assertEqual(retrieved, self.sample_data)

    def test_nonexistent_horse(self):
        """Test retrieving non-existent horse returns None."""
        result = self.db.get_horse("INVALID")
        self.assertIsNone(result)

    def test_update_performance(self):
        """Test updating horse performance data."""
        self.db.add_horse("H001", {"wins": 5, "races": 10})
        self.db.update_performance("H001", {"wins": 6, "recent_time": 65.2})
        
        updated = self.db.get_horse("H001")
        self.assertEqual(updated["wins"], 6)
        self.assertEqual(updated["recent_time"], 65.2)
        self.assertEqual(updated["races"], 10)  # Original data preserved

    def test_update_nonexistent_horse(self):
        """Test updating non-existent horse does nothing."""
        self.db.update_performance("INVALID", {"wins": 10})
        # Should not raise an error
        self.assertEqual(len(self.db), 0)

    def test_remove_horse(self):
        """Test removing horse from database."""
        self.db.add_horse("H001", self.sample_data)
        self.assertEqual(len(self.db), 1)
        
        self.db.remove_horse("H001")
        self.assertEqual(len(self.db), 0)
        self.assertIsNone(self.db.get_horse("H001"))

    def test_remove_nonexistent_horse(self):
        """Test removing non-existent horse does nothing."""
        initial_size = len(self.db)
        self.db.remove_horse("INVALID")
        self.assertEqual(len(self.db), initial_size)

    def test_list_horses(self):
        """Test listing all horse IDs."""
        horses = ["H001", "H002", "H003"]
        for horse_id in horses:
            self.db.add_horse(horse_id, self.sample_data.copy())
        
        listed_horses = self.db.list_horses()
        self.assertEqual(set(listed_horses), set(horses))

    def test_empty_database(self):
        """Test operations on empty database."""
        self.assertEqual(len(self.db), 0)
        self.assertEqual(self.db.list_horses(), [])
        self.assertIsNone(self.db.get_horse("ANY"))

class TestLeaderboard(unittest.TestCase):
    """Test cases for Leaderboard (Heap implementation)."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.leaderboard = Leaderboard()

    def test_add_result(self):
        """Test adding race results to leaderboard."""
        self.leaderboard.add_result("H001", 65.2)
        self.assertIn("H001", self.leaderboard.entries)
        self.assertEqual(self.leaderboard.size(), 1)

    def test_duplicate_prevention(self):
        """Test that duplicate horses update their best time."""
        self.leaderboard.add_result("H001", 65.2)
        self.leaderboard.add_result("H001", 63.0)  # Better time
        
        top = self.leaderboard.get_top_performers(1)
        self.assertEqual(top[0][0], 63.0)  # Better time should be kept
        self.assertEqual(self.leaderboard.size(), 1)

    def test_duplicate_worse_time(self):
        """Test that worse times don't update existing records."""
        self.leaderboard.add_result("H001", 63.0)
        self.leaderboard.add_result("H001", 65.2)  # Worse time
        
        top = self.leaderboard.get_top_performers(1)
        self.assertEqual(top[0][0], 63.0)  # Original better time preserved

    def test_top_performers_ordering(self):
        """Test that top performers are returned in correct order."""
        times = [("H001", 65.2), ("H002", 63.8), ("H003", 67.1)]
        for horse_id, time in times:
            self.leaderboard.add_result(horse_id, time)
        
        top = self.leaderboard.get_top_performers(3)
        expected_order = [63.8, 65.2, 67.1]
        actual_order = [time for time, _ in top]
        self.assertEqual(actual_order, expected_order)

    def test_get_horse_rank(self):
        """Test getting individual horse rankings."""
        times = [("H001", 65.2), ("H002", 63.8), ("H003", 67.1)]
        for horse_id, time in times:
            self.leaderboard.add_result(horse_id, time)
        
        self.assertEqual(self.leaderboard.get_horse_rank("H002"), 1)  # Fastest
        self.assertEqual(self.leaderboard.get_horse_rank("H001"), 2)  # Second
        self.assertEqual(self.leaderboard.get_horse_rank("H003"), 3)  # Third

    def test_get_rank_nonexistent_horse(self):
        """Test getting rank for non-existent horse."""
        rank = self.leaderboard.get_horse_rank("INVALID")
        self.assertEqual(rank, -1)

    def test_remove_horse(self):
        """Test removing horse from leaderboard."""
        self.leaderboard.add_result("H001", 65.2)
        self.assertTrue(self.leaderboard.remove_horse("H001"))
        self.assertEqual(self.leaderboard.size(), 0)
        self.assertNotIn("H001", self.leaderboard.entries)

    def test_remove_nonexistent_horse(self):
        """Test removing non-existent horse."""
        result = self.leaderboard.remove_horse("INVALID")
        self.assertFalse(result)

    def test_empty_leaderboard(self):
        """Test operations on empty leaderboard."""
        self.assertEqual(self.leaderboard.size(), 0)
        self.assertEqual(self.leaderboard.get_top_performers(5), [])
        self.assertEqual(self.leaderboard.get_horse_rank("ANY"), -1)

class TestAVLTree(unittest.TestCase):
    """Test cases for AVLTree (Binary Search Tree implementation)."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.tree = AVLTree()

    def test_insert_and_search(self):
        """Test inserting and searching for values."""
        self.tree.insert("H001", 0.75)
        results = self.tree.get_range(0.74, 0.76)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], ("H001", 0.75))

    def test_range_query(self):
        """Test range queries."""
        horses = [("H001", 0.8), ("H002", 0.6), ("H003", 0.9), ("H004", 0.5)]
        for horse_id, ratio in horses:
            self.tree.insert(horse_id, ratio)
        
        high_performers = self.tree.get_range(0.7, 1.0)
        expected_horses = {("H001", 0.8), ("H003", 0.9)}
        self.assertEqual(set(high_performers), expected_horses)

    def test_sorted_list(self):
        """Test getting sorted list of all entries."""
        horses = [("H001", 0.8), ("H002", 0.6), ("H003", 0.9), ("H004", 0.5)]
        for horse_id, ratio in horses:
            self.tree.insert(horse_id, ratio)
        
        sorted_list = self.tree.get_sorted_list()
        expected_order = [("H004", 0.5), ("H002", 0.6), ("H001", 0.8), ("H003", 0.9)]
        self.assertEqual(sorted_list, expected_order)

    def test_update_existing(self):
        """Test updating existing horse's win ratio."""
        self.tree.insert("H001", 0.5)
        self.tree.insert("H001", 0.8)  # Update
        
        results = self.tree.get_sorted_list()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], ("H001", 0.8))

    def test_empty_tree_operations(self):
        """Test operations on empty tree."""
        self.assertEqual(self.tree.get_range(0.0, 1.0), [])
        self.assertEqual(self.tree.get_sorted_list(), [])

    def test_single_value_range(self):
        """Test range query with single value."""
        self.tree.insert("H001", 0.75)
        results = self.tree.get_range(0.75, 0.75)
        self.assertEqual(results, [("H001", 0.75)])

    def test_large_dataset_balance(self):
        """Test that tree remains balanced with larger dataset."""
        # Insert many values to test balancing
        for i in range(20):
            horse_id = f"H{i:03d}"
            ratio = i / 20.0
            self.tree.insert(horse_id, ratio)
        
        # Tree should still function correctly
        results = self.tree.get_range(0.4, 0.6)
        expected_count = 5  # 0.4, 0.45, 0.5, 0.55, 0.6
        self.assertEqual(len(results), expected_count)

class TestIntegration(unittest.TestCase):
    """Integration tests for all data structures working together."""
    
    def setUp(self):
        """Set up all data structures for integration testing."""
        self.db = HorseDatabase()
        self.leaderboard = Leaderboard()
        self.tree = AVLTree()
        
        # Sample data
        self.horses = [
            ("H001", {"name": "Thunder", "wins": 8, "races": 10}),
            ("H002", {"name": "Lightning", "wins": 6, "races": 8}),
            ("H003", {"name": "Storm", "wins": 12, "races": 20})
        ]
        
        self.times = [("H001", 65.2), ("H002", 63.8), ("H003", 67.1)]

    def test_full_workflow(self):
        """Test complete workflow using all data structures."""
        # Add horses to database
        for horse_id, data in self.horses:
            self.db.add_horse(horse_id, data)
        
        # Add race times to leaderboard
        for horse_id, time in self.times:
            self.leaderboard.add_result(horse_id, time)
        
        # Add win ratios to tree
        for horse_id, data in self.horses:
            ratio = data["wins"] / data["races"]
            self.tree.insert(horse_id, ratio)
        
        # Test data consistency
        self.assertEqual(len(self.db), 3)
        self.assertEqual(self.leaderboard.size(), 3)
        
        # Test cross-references
        top_performer = self.leaderboard.get_top_performers(1)[0]
        horse_data = self.db.get_horse(top_performer[1])
        self.assertIsNotNone(horse_data)
        
        # Test high performers from tree exist in database
        high_performers = self.tree.get_range(0.7, 1.0)
        for horse_id, _ in high_performers:
            self.assertIsNotNone(self.db.get_horse(horse_id))

def run_tests():
    """Run all tests with detailed output."""
    # Create test suite
    test_classes = [TestHorseDatabase, TestLeaderboard, TestAVLTree, TestIntegration]
    
    suite = unittest.TestSuite()
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print(f"\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)