# Phase 1 & 2: Fundamental Data Structures
# This package contains the original implementations of core data structures

"""
Phase 1 & 2: Fundamental Data Structures

These are the basic data structures I implemented for the horse racing predictor.
Nothing fancy here - just solid implementations of the core concepts:

- HorseDatabase: Basic hash table for storing horse profiles
- Leaderboard: Min-heap to track fastest race times
- AVLTree: Self-balancing tree for querying horses by win ratio

These work fine for smaller datasets and demonstrate the fundamental concepts,
but I optimized them heavily in Phase 3 for real-world performance.

Usage:
    from phase1_phase2 import HorseDatabase, Leaderboard, AVLTree
    
    # Basic implementations
    db = HorseDatabase()
    leaderboard = Leaderboard()
    tree = AVLTree()
"""

__version__ = "2.0.0"
__author__ = "MSCS532 Student"
__status__ = "Academic Implementation"

# Import main classes for easy access
try:
    from .data_structures.hash_table import HorseDatabase
    from .data_structures.leaderboard_heap import Leaderboard
    from .data_structures.avl_tree import AVLTree
    
    __all__ = ['HorseDatabase', 'Leaderboard', 'AVLTree']
    
except ImportError:
    # Graceful handling if imports fail
    __all__ = []
