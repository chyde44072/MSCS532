# Comprehensive Test Suite for Assignment 6

This module provides thorough testing for all implemented selection algorithms and data structures to ensure correctness, robustness, and performance validation across various scenarios and edge cases.

## Test Coverage

### Selection Algorithms Testing
- **Basic Functionality**: Correct k-th element selection for various array sizes
- **Input Type Variations**: Random, sorted, reverse-sorted, and duplicate-heavy arrays
- **Edge Cases**: Empty arrays, single elements, boundary k values
- **Algorithm Consistency**: Verification that both deterministic and randomized algorithms produce identical results
- **Error Handling**: Invalid input parameter validation

### Data Structures Testing
- **Dynamic Array**: Insert, delete, access operations with automatic resizing
- **Stack Implementations**: Array-based and linked list-based stack operations
- **Queue Implementations**: Array-based (circular) and linked list-based queue operations
- **Linked List**: Insertion, deletion, search, and traversal operations
- **Rooted Tree**: Tree construction, traversals, and height calculations

### Edge Case Testing
- **Boundary Conditions**: Empty structures, single elements, maximum capacity
- **Error Conditions**: Invalid indices, empty structure operations
- **Memory Management**: Proper resizing and memory cleanup
- **Data Integrity**: Verification of data consistency after operations

## Requirements

- Python 3.7 or higher
- unittest (included with Python standard library)
- Access to implemented modules: `selection_algorithms.py`, `data_structures.py`

## How to Run

```bash
python test_assignment6.py
```

This will:
- Execute all test suites with detailed verbose output
- Report individual test results for each algorithm and data structure
- Provide comprehensive summary statistics
- Highlight any failures or errors with detailed information
- Generate a final success rate report

## Test Structure

### Test Classes
- **TestSelectionAlgorithms**: Validates both deterministic and randomized selection
- **TestDynamicArray**: Tests dynamic array operations and resizing
- **TestStackImplementations**: Validates both stack implementations
- **TestQueueImplementations**: Tests both queue implementations
- **TestSinglyLinkedList**: Comprehensive linked list operation testing
- **TestRootedTree**: Tree construction and traversal validation

### Custom Test Runner
- **Detailed Reporting**: Individual test suite success rates
- **Comprehensive Summary**: Overall statistics and coverage analysis
- **Error Analysis**: Clear identification of any implementation issues
- **Success Validation**: Confirmation of correct algorithm behavior

## Expected Output

The test suite provides:
- **Real-time Progress**: Live updates as tests execute
- **Individual Results**: Pass/fail status for each test method
- **Summary Statistics**: Total tests run, failures, errors, and success rates
- **Coverage Confirmation**: Verification that all major functionality is tested
- **Implementation Validation**: Assurance that algorithms work correctly

## Benefits

- **Quality Assurance**: Ensures implementation correctness before submission
- **Regression Testing**: Quickly identifies if changes break existing functionality
- **Educational Value**: Demonstrates proper testing practices for algorithmic code
- **Confidence Building**: Provides verification that complex algorithms work as intended
