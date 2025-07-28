# MSCS 532 Assignment 6: Medians and Order Statistics & Elementary Data Structures

## Assignment Overview

This assignment implements and analyzes algorithms for finding the k-th smallest element (order statistics) and fundamental data structures. The implementation demonstrates both theoretical understanding and practical application of these essential algorithmic concepts.

### Part 1: Selection Algorithms
- **Deterministic Selection**: Median of Medians algorithm achieving O(n) worst-case time
- **Randomized Selection**: Randomized Quickselect achieving O(n) expected time
- **Comprehensive Analysis**: Performance comparison and complexity verification

### Part 2: Elementary Data Structures
- **Simple Stack**: Clean implementation using Python list
- **Simple Queue**: Basic queue operations with straightforward approach
- **Simple Linked List**: Singly linked list with essential operations
- **Simple Tree**: Rooted tree implementation with traversal capabilities

## Project Structure

```
Assignment_6_src/
├── selection_algorithms.py              # Selection algorithms implementation
├── selection_algorithms_README.md       # Documentation for selection algorithms
├── data_structures.py                   # Data structures implementation
├── data_structures_README.md            # Documentation for data structures
├── performance_analysis.py              # Empirical performance analysis
├── performance_analysis_README.md       # Documentation for performance analysis
├── test_assignment6.py                  # Comprehensive test suite
├── test_assignment6_README.md           # Documentation for test suite
└── report.md                           # Comprehensive assignment report
```

## Key Features

### Algorithm Implementation
- **Robust Error Handling**: Comprehensive input validation and edge case management
- **Performance Tracking**: Built-in counters for comparisons, swaps, and operations
- **Educational Code**: Clear, well-documented implementations for learning
- **Empirical Validation**: Extensive testing to verify theoretical complexity

### Data Structure Design
- **Clean Implementation**: Simplified code focusing on core concepts
- **Educational Value**: Easy-to-understand implementations for learning
- **Essential Operations**: Complete API coverage for fundamental operations
- **Readable Code**: Clear structure without unnecessary complexity

### Analysis and Testing
- **Comprehensive Testing**: Unit tests covering normal operations and edge cases
- **Performance Visualization**: Graphical analysis of algorithm performance trends
- **Complexity Verification**: Empirical confirmation of theoretical time complexities
- **Practical Recommendations**: Evidence-based guidance for real-world usage

## Quick Start

### Running Individual Components

1. **Selection Algorithms Demo**:
   ```bash
   python selection_algorithms.py
   ```

2. **Data Structures Demo**:
   ```bash
   python data_structures.py
   ```

3. **Performance Analysis**:
   ```bash
   python performance_analysis.py
   ```

4. **Complete Test Suite**:
   ```bash
   python test_assignment6.py
   ```

### Requirements
- Python 3.7 or higher
- matplotlib (optional, for performance plots): `pip install matplotlib`
- numpy (optional, for enhanced analysis): `pip install numpy`

## Educational Value

This assignment demonstrates:
- **Algorithm Design**: Implementation of sophisticated selection algorithms
- **Data Structure Fundamentals**: Core concepts in computer science data organization
- **Performance Analysis**: Bridging theory and practice through empirical measurement
- **Software Engineering**: Proper testing, documentation, and code organization
- **Complexity Theory**: Practical verification of Big O notation concepts

## Implementation Highlights

### Selection Algorithms
- **Median of Medians**: Guarantees O(n) worst-case performance through careful pivot selection
- **Randomized Quickselect**: Achieves O(n) expected time with simple random pivot selection
- **Practical Optimizations**: Efficient partitioning and recursive implementation

### Data Structures
- **Dynamic Resizing**: Smart growth and shrinkage strategies for optimal memory usage
- **Multiple Implementations**: Comparative analysis of array vs. linked list approaches
- **Complete APIs**: Full feature sets matching standard library expectations
- **Performance Optimization**: Cache-conscious design for real-world efficiency

## Research and Analysis

The assignment includes comprehensive empirical analysis comparing:
- **Theoretical vs. Actual Performance**: Verification of complexity predictions
- **Implementation Trade-offs**: Memory usage, cache performance, and operation speed
- **Input Type Sensitivity**: Performance variation across different data distributions
- **Scalability Assessment**: Behavior with increasing problem sizes
