# Heapsort Implementation and Analysis

## Overview
This module implements the Heapsort algorithm using Python, providing a clear, efficient implementation that follows the correct steps for building a max-heap, extracting the maximum element, and maintaining the heap property.

## Implementation Details
- **Algorithm**: Heapsort using max-heap
- **Data Structure**: Array-based heap representation
- **Key Operations**:
  - `heapify()`: Maintains heap property
  - `build_max_heap()`: Converts array to max-heap
  - `heapsort()`: Main sorting function

## Time Complexity Analysis
- **Best Case**: O(n log n)
- **Average Case**: O(n log n)
- **Worst Case**: O(n log n)

## Space Complexity
- **Space**: O(1) - In-place sorting algorithm

## Usage
```python
from heapsort_analysis import heapsort, analyze_heapsort_performance

# Sort an array
arr = [64, 34, 25, 12, 22, 11, 90]
sorted_arr = heapsort(arr)
print(f"Sorted array: {sorted_arr}")

# Analyze performance
analyze_heapsort_performance()
```

## Files
- `heapsort_analysis.py`: Main implementation and performance analysis
