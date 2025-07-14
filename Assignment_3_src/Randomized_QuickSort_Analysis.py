import random
import time

def randomized_quicksort(arr):
    """
    Randomized Quicksort implementation.
    Chooses a random pivot for each partition.
    Handles empty arrays, repeated elements, and already sorted arrays.
    """
    if len(arr) <= 1:
        return arr
    pivot_index = random.randint(0, len(arr) - 1)
    pivot = arr[pivot_index]
    less = [x for i, x in enumerate(arr) if x < pivot or (x == pivot and i != pivot_index)]
    equal = [x for i, x in enumerate(arr) if x == pivot and i == pivot_index]
    greater = [x for x in arr if x > pivot]
    return randomized_quicksort(less) + equal + randomized_quicksort(greater)

def deterministic_quicksort(arr):
    """
    Deterministic Quicksort implementation.
    Always chooses the first element as the pivot.
    """
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    less = [x for x in arr[1:] if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr[1:] if x > pivot]
    return deterministic_quicksort(less) + equal + deterministic_quicksort(greater)

# Example usage and empirical comparison
if __name__ == "__main__":
    import numpy as np

    sizes = [1000, 5000, 10000]
    distributions = {
        "Random": lambda n: np.random.randint(0, 10000, n).tolist(),
        "Sorted": lambda n: list(range(n)),
        "Reverse": lambda n: list(range(n, 0, -1)),
        "Repeated": lambda n: [random.choice([1, 2, 3, 4, 5]) for _ in range(n)]
    }

    for size in sizes:
        print(f"\nArray size: {size}")
        for name, gen in distributions.items():
            arr = gen(size)
            arr_copy = arr.copy()

            start = time.time()
            randomized_quicksort(arr)
            rand_time = time.time() - start

            start = time.time()
            deterministic_quicksort(arr_copy)
            det_time = time.time() - start

            print(f"{name:10} | Randomized: {rand_time:.5f}s | Deterministic: {det_time:.5f}s")


