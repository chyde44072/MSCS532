def insertion_sort_desc(arr):
    """
    Sorts the array in-place in decreasing order using insertion sort.
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] < key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

# Example usage
if __name__ == "__main__":
    test_data = [8, 3, 5, 2, 9]
    insertion_sort_desc(test_data)
    print("Sorted (descending):", test_data)

