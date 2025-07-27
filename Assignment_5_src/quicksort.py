import random
from typing import List, Tuple
import time


class QuickSort:
    """
    A class implementing both deterministic and randomized versions of Quicksort algorithm.
    
    The class provides methods for:
    - Deterministic Quicksort (using last element as pivot)
    - Randomized Quicksort (using random pivot selection)
    - Performance tracking and analysis
    """
    
    def __init__(self):
        self.comparisons = 0
        self.swaps = 0
        self.recursive_calls = 0
    
    def reset_counters(self):
        """Reset performance tracking counters."""
        self.comparisons = 0
        self.swaps = 0
        self.recursive_calls = 0
    
    def get_performance_stats(self) -> dict:
        """Return current performance statistics."""
        return {
            'comparisons': self.comparisons,
            'swaps': self.swaps,
            'recursive_calls': self.recursive_calls
        }
    
    def deterministic_quicksort(self, arr: List[int], low: int = 0, high: int = None) -> List[int]:
        """
        Deterministic Quicksort implementation using the last element as pivot.
        
        Time Complexity:
        - Best Case: O(n log n) - when pivot divides array into equal halves
        - Average Case: O(n log n) - on average, pivot provides good division
        - Worst Case: O(n²) - when pivot is always smallest/largest element
        
        Space Complexity: O(log n) average case, O(n) worst case (due to recursion stack)
        
        Args:
            arr: List of integers to sort
            low: Starting index of subarray
            high: Ending index of subarray
            
        Returns:
            Sorted list of integers
        """
        if high is None:
            high = len(arr) - 1
            self.reset_counters()
        
        # Base case: if subarray has 1 or 0 elements, it's already sorted
        if low < high:
            self.recursive_calls += 1
            
            # Partition the array and get the pivot index
            pivot_index = self._partition_deterministic(arr, low, high)
            
            # Recursively sort elements before and after partition
            self.deterministic_quicksort(arr, low, pivot_index - 1)
            self.deterministic_quicksort(arr, pivot_index + 1, high)
        
        return arr
    
    def randomized_quicksort(self, arr: List[int], low: int = 0, high: int = None) -> List[int]:
        """
        Randomized Quicksort implementation using random pivot selection.
        
        Time Complexity:
        - Expected Case: O(n log n) - randomization makes worst case highly unlikely
        - Worst Case: O(n²) - theoretically possible but probability is 1/n!
        
        Space Complexity: O(log n) expected case
        
        The randomization significantly reduces the probability of encountering
        the worst-case scenario, making the algorithm more reliable in practice.
        
        Args:
            arr: List of integers to sort
            low: Starting index of subarray
            high: Ending index of subarray
            
        Returns:
            Sorted list of integers
        """
        if high is None:
            high = len(arr) - 1
            self.reset_counters()
        
        if low < high:
            self.recursive_calls += 1
            
            # Partition the array with random pivot and get the pivot index
            pivot_index = self._partition_randomized(arr, low, high)
            
            # Recursively sort elements before and after partition
            self.randomized_quicksort(arr, low, pivot_index - 1)
            self.randomized_quicksort(arr, pivot_index + 1, high)
        
        return arr
    
    def _partition_deterministic(self, arr: List[int], low: int, high: int) -> int:
        """
        Partition function for deterministic quicksort using last element as pivot.
        
        This function places the pivot element at its correct position in sorted array,
        and places all smaller elements to left of pivot and all greater elements to right.
        
        Args:
            arr: Array to partition
            low: Starting index
            high: Ending index
            
        Returns:
            Index of pivot element after partitioning
        """
        # Choose the rightmost element as pivot
        pivot = arr[high]
        
        # Index of smaller element (indicates right position of pivot found so far)
        i = low - 1
        
        for j in range(low, high):
            self.comparisons += 1
            
            # If current element is smaller than or equal to pivot
            if arr[j] <= pivot:
                i += 1
                if i != j:  # Only swap if indices are different
                    arr[i], arr[j] = arr[j], arr[i]
                    self.swaps += 1
        
        # Place pivot at correct position
        if i + 1 != high:  # Only swap if indices are different
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            self.swaps += 1
        
        return i + 1
    
    def _partition_randomized(self, arr: List[int], low: int, high: int) -> int:
        """
        Partition function for randomized quicksort using random pivot selection.
        
        This function randomly selects a pivot, swaps it with the last element,
        and then uses the same partitioning logic as deterministic version.
        
        Args:
            arr: Array to partition
            low: Starting index
            high: Ending index
            
        Returns:
            Index of pivot element after partitioning
        """
        # Randomly choose a pivot from the current subarray
        random_index = random.randint(low, high)
        
        # Swap the randomly chosen element with the last element
        if random_index != high:
            arr[random_index], arr[high] = arr[high], arr[random_index]
            self.swaps += 1
        
        # Now use the same partition logic as deterministic version
        return self._partition_deterministic(arr, low, high)


def time_sorting_algorithm(sort_func, arr: List[int]) -> Tuple[float, List[int], dict]:
    """
    Time a sorting algorithm and return execution time, sorted array, and performance stats.
    
    Args:
        sort_func: Sorting function to time
        arr: Array to sort (will be copied to avoid modifying original)
        
    Returns:
        Tuple of (execution_time, sorted_array, performance_stats)
    """
    arr_copy = arr.copy()
    start_time = time.time()
    sorted_arr = sort_func(arr_copy)
    end_time = time.time()
    
    return end_time - start_time, sorted_arr, sort_func.__self__.get_performance_stats()


def demonstrate_quicksort():
    """
    Demonstrate both versions of Quicksort with a sample array.
    """
    print("=== Quicksort Algorithm Demonstration ===\n")
    
    # Sample data for demonstration
    test_array = [64, 34, 25, 12, 22, 11, 90, 88, 76, 50, 42]
    print(f"Original array: {test_array}")
    print()
    
    # Create QuickSort instance
    qs = QuickSort()
    
    # Test deterministic quicksort
    print("1. Deterministic Quicksort:")
    exec_time, sorted_det, stats_det = time_sorting_algorithm(
        qs.deterministic_quicksort, test_array
    )
    print(f"   Sorted array: {sorted_det}")
    print(f"   Execution time: {exec_time:.6f} seconds")
    print(f"   Performance stats: {stats_det}")
    print()
    
    # Test randomized quicksort
    print("2. Randomized Quicksort:")
    exec_time, sorted_rand, stats_rand = time_sorting_algorithm(
        qs.randomized_quicksort, test_array
    )
    print(f"   Sorted array: {sorted_rand}")
    print(f"   Execution time: {exec_time:.6f} seconds")
    print(f"   Performance stats: {stats_rand}")
    print()
    
    # Verify correctness
    print("3. Verification:")
    print(f"   Both algorithms produce same result: {sorted_det == sorted_rand}")
    print(f"   Result matches Python's sorted(): {sorted_det == sorted(test_array)}")


if __name__ == "__main__":
    demonstrate_quicksort()
