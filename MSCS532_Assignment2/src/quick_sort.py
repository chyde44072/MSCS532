import time
import tracemalloc
import random

# Quick Sort implementation
def quick_sort(arr):
    # Base case: arrays with 0 or 1 element are already sorted
    if len(arr) <= 1:
        return arr
    # Choose the pivot
    pivot = arr[len(arr) // 2]
    # Partition the array into less, equal, and greater lists
    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]
    # Recursively sort the partitions and combine
    return quick_sort(less) + equal + quick_sort(greater)

if __name__ == "__main__":
    # Prepare datasets: sorted, reverse sorted, and random
    sorted_data = list(range(25))
    reverse_sorted_data = list(range(25, 0, -1))
    random_data = [random.randint(0, 25) for _ in range(25)]

    datasets = {
        "Sorted": sorted_data,
        "Reverse Sorted": reverse_sorted_data,
        "Random": random_data
    }

    # Test quick sort on each dataset and measure performance
    for description, data in datasets.items():
        print(f"\n{description} numbers:", data)

        # Start memory tracking
        tracemalloc.start()
        start_time = time.perf_counter()
        # Perform Quick Sort
        sorted_result = quick_sort(data)
        end_time = time.perf_counter()
        current_mem, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(f"Sorted {description} numbers:", sorted_result)
        print(f"Execution time for {description}: {end_time - start_time:.6f} seconds")
        print(f"Peak memory usage for {description}: {peak_mem / 1024:.2f} KB")