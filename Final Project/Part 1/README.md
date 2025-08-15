# Matrix Multiplication Optimization Demo

This project demonstrates the impact of data structure optimization on performance in high-performance computing (HPC) using Python. It compares a naive matrix multiplication implementation using Python lists with an optimized version using NumPy arrays.

## Files
- `matrix_optimization_demo.py`: Python script containing both implementations and benchmarking code.

## How It Works
- The script multiplies two randomly generated 300x300 matrices using:
  1. A naive approach with Python lists and nested loops
  2. An optimized approach with NumPy's `dot` function
- It measures and prints the execution time for both methods.

## Usage
1. Install NumPy if needed:
   ```
pip install numpy
   ```
2. Run the script:
   ```
python matrix_optimization_demo.py
   ```
3. View the output in your terminal to compare performance.

## Results
- The NumPy-based approach is significantly faster due to better memory access patterns and vectorized operations.

## Reference
This demo is based on optimization techniques discussed in:
- Azad, M. A. K., Iqbal, N., Hassan, F., & Roy, P. (2022). An Empirical Study of High Performance Computing (HPC) Performance Bugs. University of Michigan - Dearborn.


