"""""
This module implements the Heapsort algorithm and provides comprehensive analysis
of its performance characteristics compared to other sorting algorithms.
"""

import time
import random
from typing import List, Tuple, Dict


def heapify(arr: List[int], n: int, i: int) -> None:
    """
    Maintain the max-heap property for a subtree rooted at index i.
    
    Args:
        arr: The array representing the heap
        n: Size of the heap
        i: Root index of the subtree
    """
    largest = i  # Initialize largest as root
    left = 2 * i + 1  # Left child
    right = 2 * i + 2  # Right child
    
    # Check if left child exists and is greater than root
    if left < n and arr[left] > arr[largest]:
        largest = left
    
    # Check if right child exists and is greater than largest so far
    if right < n and arr[right] > arr[largest]:
        largest = right
    
    # If largest is not root, swap and recursively heapify
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def build_max_heap(arr: List[int]) -> None:
    """
    Build a max-heap from an unsorted array.
    
    Args:
        arr: The array to convert to a max-heap
    """
    n = len(arr)
    # Start from the last non-leaf node and heapify each node
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)


def heapsort(arr: List[int]) -> List[int]:
    """
    Sort an array using the heapsort algorithm.
    
    Args:
        arr: The array to sort
        
    Returns:
        A new sorted array
    """
    # Create a copy to avoid modifying the original array
    sorted_arr = arr.copy()
    n = len(sorted_arr)
    
    # Build max-heap
    build_max_heap(sorted_arr)
    
    # Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        # Move current root to end
        sorted_arr[0], sorted_arr[i] = sorted_arr[i], sorted_arr[0]
        
        # Call heapify on the reduced heap
        heapify(sorted_arr, i, 0)
    
    return sorted_arr


def quicksort(arr: List[int]) -> List[int]:
    """
    Quick implementation of quicksort for comparison.
    
    Args:
        arr: The array to sort
        
    Returns:
        A new sorted array
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quicksort(left) + middle + quicksort(right)


def merge_sort(arr: List[int]) -> List[int]:
    """
    Implementation of merge sort for comparison.
    
    Args:
        arr: The array to sort
        
    Returns:
        A new sorted array
    """
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)


def merge(left: List[int], right: List[int]) -> List[int]:
    """Helper function for merge sort."""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def generate_test_data(size: int, data_type: str) -> List[int]:
    """
    Generate test data of different types.
    
    Args:
        size: Size of the array
        data_type: Type of data ('random', 'sorted', 'reverse', 'duplicates')
        
    Returns:
        Generated test array
    """
    if data_type == 'random':
        return [random.randint(1, 1000) for _ in range(size)]
    elif data_type == 'sorted':
        return list(range(1, size + 1))
    elif data_type == 'reverse':
        return list(range(size, 0, -1))
    elif data_type == 'duplicates':
        return [random.randint(1, 10) for _ in range(size)]
    else:
        raise ValueError(f"Unknown data type: {data_type}")


def measure_sorting_time(sort_func, arr: List[int]) -> float:
    """
    Measure the execution time of a sorting function.
    
    Args:
        sort_func: The sorting function to test
        arr: The array to sort
        
    Returns:
        Execution time in seconds
    """
    start_time = time.time()
    sort_func(arr.copy())
    return time.time() - start_time


def compare_sorting_algorithms() -> Dict[str, Dict[str, List[float]]]:
    """
    Compare heapsort with quicksort and merge sort on different input types.
    
    Returns:
        Dictionary containing timing results
    """
    algorithms = {
        'Heapsort': heapsort,
        'Quicksort': quicksort,
        'Merge Sort': merge_sort
    }
    
    data_types = ['random', 'sorted', 'reverse', 'duplicates']
    sizes = [100, 500, 1000, 2000, 5000]
    
    results = {alg: {dt: [] for dt in data_types} for alg in algorithms}
    
    print("Comparing sorting algorithms...")
    print("-" * 50)
    
    for data_type in data_types:
        print(f"\nTesting {data_type} data:")
        for size in sizes:
            print(f"  Size: {size}")
            test_data = generate_test_data(size, data_type)
            
            for alg_name, alg_func in algorithms.items():
                avg_time = 0
                # Run multiple times for more accurate measurement
                for _ in range(3):
                    avg_time += measure_sorting_time(alg_func, test_data)
                avg_time /= 3
                
                results[alg_name][data_type].append(avg_time)
                print(f"    {alg_name}: {avg_time:.6f}s")
    
    return results


def analyze_heapsort_performance():
    """
    Comprehensive analysis of heapsort performance.
    """
    print("=" * 60)
    print("HEAPSORT IMPLEMENTATION AND ANALYSIS")
    print("=" * 60)
    
    # Test basic functionality
    print("\n1. Basic Functionality Test:")
    test_arrays = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 2, 8, 1, 9],
        [1],
        [],
        [3, 3, 3, 3]
    ]
    
    for arr in test_arrays:
        sorted_arr = heapsort(arr)
        print(f"Original: {arr}")
        print(f"Sorted:   {sorted_arr}")
        print(f"Correct:  {sorted_arr == sorted(arr)}")
        print()
    
    # Performance comparison
    print("\n2. Performance Comparison:")
    results = compare_sorting_algorithms()
    
    # Analysis summary
    print("\n3. Time Complexity Analysis:")
    print("Heapsort Complexity:")
    print("- Best Case:    O(n log n)")
    print("- Average Case: O(n log n)")
    print("- Worst Case:   O(n log n)")
    print("- Space:        O(1) - in-place sorting")
    print()
    
    print("Key Observations:")
    print("- Heapsort has consistent O(n log n) performance regardless of input")
    print("- Unlike quicksort, it doesn't degrade to O(n²) in worst case")
    print("- More predictable than quicksort but often slower in practice")
    print("- Uses constant extra space unlike merge sort's O(n) space")
    
    return results


def visualize_heap_construction():
    """
    Demonstrate heap construction process.
    """
    print("\n4. Heap Construction Demonstration:")
    arr = [4, 10, 3, 5, 1, 2]
    print(f"Original array: {arr}")
    
    # Build heap step by step
    n = len(arr)
    print(f"\nBuilding max-heap:")
    print(f"Starting from last non-leaf node (index {n // 2 - 1}):")
    
    for i in range(n // 2 - 1, -1, -1):
        print(f"  Heapifying subtree rooted at index {i}")
        heapify(arr, n, i)
        print(f"  Array after heapifying: {arr}")
    
    print(f"\nFinal max-heap: {arr}")


if __name__ == "__main__":
    # Run comprehensive analysis
    results = analyze_heapsort_performance()
    
    # Demonstrate heap construction
    visualize_heap_construction()
    
    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)
