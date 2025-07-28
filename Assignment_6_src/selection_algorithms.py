"""
This module implements both deterministic and randomized selection algorithms
for finding the k-th smallest element in an array.

Algorithms implemented:
1. Deterministic Selection (Median of Medians) - O(n) worst-case
2. Randomized Selection (Randomized Quickselect) - O(n) expected time
"""

import random
import time
from typing import List, Tuple


class SelectionAlgorithms:
    """
    A class implementing various selection algorithms for finding the k-th smallest element.
    """
    
    def __init__(self):
        self.comparisons = 0
        self.swaps = 0
        
    def reset_counters(self):
        """Reset performance counters."""
        self.comparisons = 0
        self.swaps = 0
    
    def get_stats(self) -> Tuple[int, int]:
        """Return current performance statistics."""
        return self.comparisons, self.swaps
    
    def partition(self, arr: List[int], low: int, high: int, pivot: int) -> int:
        """
        Partition array around a given pivot element.
        
        Args:
            arr: Array to partition
            low: Starting index
            high: Ending index
            pivot: Pivot element value
            
        Returns:
            Final position of pivot element
        """
        # Find pivot index and move to end
        pivot_idx = -1
        for i in range(low, high + 1):
            self.comparisons += 1
            if arr[i] == pivot:
                pivot_idx = i
                break
        
        if pivot_idx != -1:
            arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
            self.swaps += 1
        
        # Standard partition logic
        i = low - 1
        for j in range(low, high):
            self.comparisons += 1
            if arr[j] <= pivot:
                i += 1
                if i != j:
                    arr[i], arr[j] = arr[j], arr[i]
                    self.swaps += 1
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        self.swaps += 1
        return i + 1
    
    def find_median_of_medians(self, arr: List[int], low: int, high: int) -> int:
        """
        Find median of medians for deterministic pivot selection.
        
        Args:
            arr: Array to find median of medians
            low: Starting index
            high: Ending index
            
        Returns:
            Median of medians value
        """
        n = high - low + 1
        
        # Base case: if 5 or fewer elements, return median directly
        if n <= 5:
            sub_arr = sorted(arr[low:high + 1])
            self.comparisons += n * (n - 1) // 2  # Approximate comparisons for sorting
            return sub_arr[n // 2]
        
        # Divide into groups of 5 and find medians
        medians = []
        for i in range(low, high + 1, 5):
            group_high = min(i + 4, high)
            group = sorted(arr[i:group_high + 1])
            self.comparisons += len(group) * (len(group) - 1) // 2
            medians.append(group[len(group) // 2])
        
        # Recursively find median of medians
        return self.deterministic_select(medians, 0, len(medians) - 1, len(medians) // 2)
    
    def deterministic_select(self, arr: List[int], low: int, high: int, k: int) -> int:
        """
        Deterministic selection algorithm (Median of Medians).
        Finds k-th smallest element in O(n) worst-case time.
        
        Args:
            arr: Array to search in
            low: Starting index
            high: Ending index
            k: Target rank (0-indexed)
            
        Returns:
            k-th smallest element
        """
        if low == high:
            return arr[low]
        
        # Find median of medians as pivot
        pivot = self.find_median_of_medians(arr, low, high)
        
        # Partition around pivot
        pivot_idx = self.partition(arr, low, high, pivot)
        
        # Determine which side to recurse on
        if k == pivot_idx:
            return arr[pivot_idx]
        elif k < pivot_idx:
            return self.deterministic_select(arr, low, pivot_idx - 1, k)
        else:
            return self.deterministic_select(arr, pivot_idx + 1, high, k)
    
    def randomized_select(self, arr: List[int], low: int, high: int, k: int) -> int:
        """
        Randomized selection algorithm (Randomized Quickselect).
        Finds k-th smallest element in O(n) expected time.
        
        Args:
            arr: Array to search in
            low: Starting index
            high: Ending index
            k: Target rank (0-indexed)
            
        Returns:
            k-th smallest element
        """
        if low == high:
            return arr[low]
        
        # Random pivot selection
        pivot_idx = random.randint(low, high)
        pivot = arr[pivot_idx]
        
        # Partition around pivot
        pivot_idx = self.partition(arr, low, high, pivot)
        
        # Determine which side to recurse on
        if k == pivot_idx:
            return arr[pivot_idx]
        elif k < pivot_idx:
            return self.randomized_select(arr, low, pivot_idx - 1, k)
        else:
            return self.randomized_select(arr, pivot_idx + 1, high, k)
    
    def find_kth_smallest_deterministic(self, arr: List[int], k: int) -> int:
        """
        Public interface for deterministic selection.
        
        Args:
            arr: Input array
            k: Target rank (1-indexed)
            
        Returns:
            k-th smallest element
        """
        if not arr or k < 1 or k > len(arr):
            raise ValueError("Invalid input: empty array or k out of bounds")
        
        arr_copy = arr.copy()
        self.reset_counters()
        return self.deterministic_select(arr_copy, 0, len(arr_copy) - 1, k - 1)
    
    def find_kth_smallest_randomized(self, arr: List[int], k: int) -> int:
        """
        Public interface for randomized selection.
        
        Args:
            arr: Input array
            k: Target rank (1-indexed)
            
        Returns:
            k-th smallest element
        """
        if not arr or k < 1 or k > len(arr):
            raise ValueError("Invalid input: empty array or k out of bounds")
        
        arr_copy = arr.copy()
        self.reset_counters()
        return self.randomized_select(arr_copy, 0, len(arr_copy) - 1, k - 1)


def demonstrate_selection_algorithms():
    """Demonstrate both selection algorithms with sample data."""
    print("=" * 60)
    print("SELECTION ALGORITHMS DEMONSTRATION")
    print("=" * 60)
    
    # Test cases
    test_cases = [
        ([3, 6, 8, 10, 1, 2, 1], 3, "Small array with duplicates"),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5, "Sorted array"),
        ([10, 9, 8, 7, 6, 5, 4, 3, 2, 1], 7, "Reverse sorted array"),
        ([5, 5, 5, 5, 5], 3, "All elements same"),
        (list(range(1, 101)), 50, "Larger array (1-100)")
    ]
    
    selector = SelectionAlgorithms()
    
    for i, (arr, k, description) in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {description}")
        print(f"Array: {arr if len(arr) <= 20 else f'[{arr[0]}, {arr[1]}, ..., {arr[-2]}, {arr[-1]}] (length: {len(arr)})'}")
        print(f"Finding {k}-th smallest element")
        
        # Deterministic selection
        start_time = time.perf_counter()
        result_det = selector.find_kth_smallest_deterministic(arr, k)
        det_time = time.perf_counter() - start_time
        det_comparisons, det_swaps = selector.get_stats()
        
        # Randomized selection
        start_time = time.perf_counter()
        result_rand = selector.find_kth_smallest_randomized(arr, k)
        rand_time = time.perf_counter() - start_time
        rand_comparisons, rand_swaps = selector.get_stats()
        
        print(f"Deterministic result: {result_det} (Time: {det_time:.6f}s, Comparisons: {det_comparisons}, Swaps: {det_swaps})")
        print(f"Randomized result:    {result_rand} (Time: {rand_time:.6f}s, Comparisons: {rand_comparisons}, Swaps: {rand_swaps})")
        
        # Verify correctness
        sorted_arr = sorted(arr)
        expected = sorted_arr[k-1]
        print(f"Expected result:      {expected}")
        print(f"Correctness: {'✓' if result_det == result_rand == expected else '✗'}")


if __name__ == "__main__":
    # Set random seed for reproducible results
    random.seed(42)
    demonstrate_selection_algorithms()
