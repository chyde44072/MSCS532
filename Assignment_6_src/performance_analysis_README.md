# Performance Analysis Tool

This module provides comprehensive empirical analysis of the implemented selection algorithms and data structures, comparing theoretical predictions with actual performance measurements through systematic testing and visualization.

## Analysis Features

### Selection Algorithms Analysis
- **Deterministic vs Randomized**: Compare Median of Medians with Randomized Quickselect
- **Input Type Variations**: Test on random, sorted, reverse-sorted, and duplicate-heavy data
- **Scalability Testing**: Measure performance across different input sizes (100 to 10,000 elements)
- **Statistical Metrics**: Track comparisons, swaps, and execution times

### Data Structures Analysis
- **Implementation Comparisons**: Array-based vs Linked List-based stacks and queues
- **Operation Complexity**: Measure insert, delete, and access operations
- **Memory Efficiency**: Compare space usage and cache performance
- **Scalability Assessment**: Test performance with increasing data sizes

### Visualization
- **Performance Plots**: Generate comprehensive charts showing time complexity trends
- **Comparative Analysis**: Side-by-side performance comparisons
- **Growth Rate Analysis**: Verify theoretical complexity predictions

## Requirements

- Python 3.7 or higher
- matplotlib (optional, for plot generation): `pip install matplotlib`
- numpy (optional, for enhanced analysis): `pip install numpy`

## How to Run

```bash
python performance_analysis.py
```

This will:
- Run comprehensive performance tests on all algorithms and data structures
- Generate detailed timing and operation count statistics
- Create performance visualization plots (if matplotlib is available)
- Provide a summary report with empirical complexity analysis
- Compare theoretical predictions with observed performance

## Output

The analysis generates:
- **Console Output**: Detailed performance metrics and comparison tables
- **Summary Report**: Comprehensive analysis of complexity verification
- **Performance Plots**: Visual representation of algorithm performance (performance_analysis.png)
- **Recommendations**: Practical guidance for algorithm and data structure selection

## Key Insights

- **Linear Time Verification**: Confirms O(n) performance of selection algorithms
- **Implementation Trade-offs**: Quantifies differences between array and linked implementations
- **Cache Performance**: Demonstrates impact of memory access patterns
- **Practical Guidelines**: Evidence-based recommendations for real-world usage
