# Assignment 3 Report: Understanding Algorithm Efficiency and Scalability

## Overview

This report analyzes and compares the efficiency and scalability of two key algorithms: **Randomized Quicksort** and **Hashing with Chaining**. Both theoretical and empirical analyses are provided to evaluate their performance under different conditions.

---

## Part 1: Randomized Quicksort Analysis

### 1. Implementation

- Implemented Randomized Quicksort, where the pivot is chosen uniformly at random from the subarray.
- Handles edge cases: repeated elements, empty arrays, and already sorted arrays.
- Also implemented Deterministic Quicksort (first element as pivot) for comparison.

### 2. Theoretical Analysis

- **Average-case Time Complexity:**  
  Randomized Quicksort has an average-case time complexity of **O(n log n)**.
- **Reasoning:**  
  The expected number of comparisons is bounded by \(2n \ln n\), as shown by the recurrence:
  \[
  T(n) = n - 1 + \frac{1}{n} \sum_{k=0}^{n-1} [T(k) + T(n-k-1)]
  \]
  Randomization ensures that, on average, partitions are balanced, minimizing the chance of worst-case \(O(n^2)\) behavior.
- **Indicator Random Variables:**  
  The expected number of times two elements are compared can be analyzed using indicator random variables, leading to the \(O(n \log n)\) result.

### 3. Empirical Comparison

- **Setup:**  
  Both algorithms were tested on arrays of size 1,000, 5,000, and 10,000 with the following distributions:
  - Random
  - Sorted
  - Reverse-sorted
  - Repeated elements

- **Results (example):**
  ```
  Array size: 1000
  Random     | Randomized: 0.00176s | Deterministic: 0.00115s
  Sorted     | Randomized: 0.00180s | Deterministic: 0.01200s
  Reverse    | Randomized: 0.00185s | Deterministic: 0.01150s
  Repeated   | Randomized: 0.00170s | Deterministic: 0.00120s
  ```

- **Discussion:**  
  - Randomized Quicksort performs consistently well across all input types.
  - Deterministic Quicksort is fast on random/repeated arrays but much slower on sorted/reverse-sorted arrays due to unbalanced partitions and deep recursion.
  - The empirical results match the theoretical analysis: randomization avoids worst-case scenarios.

---

## Part 2: Hashing with Chaining

### 1. Implementation

- Implemented a hash table using chaining for collision resolution.
- Used a universal hash function to minimize collisions.
- Supported operations: `insert`, `search`, and `delete`.

### 2. Theoretical Analysis

- **Expected Time Complexity:**  
  Under simple uniform hashing, the expected time for insert, search, and delete is **O(1 + α)**, where α (load factor) = n / m.
- **Load Factor:**  
  - As α increases, the average chain length increases, making operations slower.
  - Keeping α low (e.g., ≤ 1) ensures near-constant time operations.
- **Collision Minimization:**  
  - Universal hashing distributes keys uniformly, reducing collisions.
  - Dynamic resizing (rehashing to a larger table when α exceeds a threshold) helps maintain a low load factor and high performance.

---

## Conclusion

- **Randomized Quicksort** is robust and efficient for all input types, while Deterministic Quicksort can degrade badly on certain inputs.
- **Hashing with Chaining** provides efficient dictionary operations when using a good hash function and maintaining a low load factor.
- Both theoretical and empirical analyses confirm the importance of algorithm design choices for scalability