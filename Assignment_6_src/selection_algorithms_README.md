# Selection Algorithms Implementation and Analysis

This module implements both deterministic and randomized selection algorithms for finding the k-th smallest element in an array, demonstrating the theoretical and practical differences between worst-case and expected-case linear time algorithms.

## Algorithms Implemented

### 1. Deterministic Selection (Median of Medians)
- **Time Complexity**: O(n) worst-case
- **Space Complexity**: O(log n) due to recursion
- **Key Feature**: Guarantees linear time performance regardless of input

### 2. Randomized Selection (Randomized Quickselect)
- **Time Complexity**: O(n) expected, O(n²) worst-case
- **Space Complexity**: O(log n) expected due to recursion
- **Key Feature**: Simple implementation with excellent average performance

## Requirements

- Python 3.7 or higher
- No external dependencies required

## How to Run

```bash
python selection_algorithms.py
```

This will:
- Demonstrate both deterministic and randomized selection on various test cases
- Show performance statistics (comparisons, swaps)
- Display execution times for comparison
- Verify correctness of both implementations
- Highlight the trade-offs between guaranteed and expected performance

## Key Features

- **Robust Implementation**: Handles edge cases including duplicates and boundary conditions
- **Performance Tracking**: Monitors comparisons and swaps for empirical analysis
- **Comprehensive Testing**: Multiple test scenarios including sorted, reverse-sorted, and random data
- **Educational Focus**: Clear code structure for understanding algorithmic concepts
