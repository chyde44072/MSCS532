"""
Matrix Multiplication Optimization Demo
Shows the impact of memory access optimization in HPC using Python lists vs NumPy arrays.
"""
import time
import numpy as np

# Naive matrix multiplication using lists
def matmul_lists(A, B):
    n = len(A)
    m = len(B[0])
    p = len(B)
    result = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

# Optimized matrix multiplication using NumPy
def matmul_numpy(A, B):
    return np.dot(A, B)

# Generate random matrices
size = 300  # Keep size moderate for demo
A_list = [[float(i * j % 10) for j in range(size)] for i in range(size)]
B_list = [[float(i * j % 7) for j in range(size)] for i in range(size)]
A_np = np.array(A_list)
B_np = np.array(B_list)

# Time naive list multiplication
start = time.time()
matmul_lists(A_list, B_list)
end = time.time()
print(f"Naive lists multiplication time: {end - start:.4f} seconds")

# Time NumPy multiplication
start = time.time()
matmul_numpy(A_np, B_np)
end = time.time()
print(f"NumPy multiplication time: {end - start:.4f} seconds")

# Results show the impact of memory access optimization
