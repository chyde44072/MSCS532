import time
import tracemalloc
import random

# Merge Sort implementation
def merge_sort(arr):
    # Base case: arrays with 0 or 1 element are already sorted
    if len(arr) <= 1:
        return arr
    # Split the array into two halves
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    # Merge the sorted halves
    return merge(left, right)

def merge(left, right):
    # Merge two sorted arrays into one sorted array
    result = []
    i = j = 0
    # Compare elements from both arrays and add the smallest to result
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    # Add any remaining elements from left or right
    result.extend(left[i:])
    result.extend(right[j:])
    return result

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

    # Test merge sort on each dataset and measure performance
    for description, data in datasets.items():
        print(f"\n{description} numbers:", data)

        # Start memory tracking
        tracemalloc.start()  
        start_time = time.perf_counter() 
        # Perform Merge Sort 
        sorted_result = merge_sort(data)
        end_time = time.perf_counter()    
        current_mem, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()  

        print(f"Sorted {description} numbers:", sorted_result)
        print(f"Execution time for {description}: {end_time - start_time:.6f} seconds")
        print(f"Peak memory usage for {description}: {peak_mem / 1024:.2f} KB")