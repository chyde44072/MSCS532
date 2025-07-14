# Priority Queue Implementation

## Overview
This module implements a binary heap-based priority queue for task scheduling applications. The implementation supports both max-heap and min-heap operations with a focus on efficient task management.

## Implementation Details
- **Data Structure**: Array-based binary heap
- **Task Representation**: Task class with ID, priority, arrival time, and deadline
- **Heap Type**: Configurable (max-heap or min-heap)

## Core Operations
- `insert(task)`: Insert new task - O(log n)
- `extract_max/min()`: Remove highest/lowest priority task - O(log n)
- `increase/decrease_key()`: Modify task priority - O(log n)
- `is_empty()`: Check if queue is empty - O(1)

## Applications
- Task scheduling systems
- Job queue management
- Priority-based resource allocation

## Usage
```python
from priority_queue_implementation import PriorityQueue, Task

# Create priority queue
pq = PriorityQueue(max_heap=True)

# Create and insert tasks
task1 = Task(1, priority=5, arrival_time=0, deadline=10)
pq.insert(task1)

# Extract highest priority task
next_task = pq.extract_max()
```

## Files
- `priority_queue_implementation.py`: Main implementation
- `task_scheduler_simulation.py`: Simulation and testing
