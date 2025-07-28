# Elementary Data Structures Implementation and Analysis

This module implements fundamental data structures with simplified, clean implementations that demonstrate core concepts while maintaining readability and educational value.

## Data Structures Implemented

### 1. SimpleStack
- **Implementation**: Using Python list for simplicity
- **Operations**: push, pop, peek, is_empty, size
- **Time Complexity**: O(1) for all operations
- **Space Complexity**: O(n)

### 2. SimpleQueue
- **Implementation**: Using Python list (simple but O(n) dequeue)
- **Operations**: enqueue, dequeue, peek, is_empty, size
- **Time Complexity**: 
  - enqueue: O(1)
  - dequeue: O(n) (simple implementation)
- **Space Complexity**: O(n)

### 3. SimpleLinkedList
- **Implementation**: Singly linked list with head pointer
- **Operations**: insert_front, insert_back, delete_front, search, to_list
- **Time Complexity**:
  - Insert at front: O(1)
  - Insert at back: O(n)
  - Delete front: O(1)
  - Search: O(n)
- **Space Complexity**: O(n)

### 4. SimpleTree
- **Implementation**: Rooted tree using nodes with children lists
- **Operations**: add_child, preorder traversal
- **Time Complexity**: O(n) for most operations
- **Space Complexity**: O(n)

## Requirements

- Python 3.7 or higher
- No external dependencies required

## How to Run

```bash
python data_structures.py
```

This will:
- Demonstrate all data structure implementations with sample operations
- Show basic operations for stacks, queues, linked lists, and trees
- Display simple examples of each data structure in action
- Highlight the core concepts and time complexities

## Key Features

- **Simple Implementations**: Clean, readable code focusing on core concepts
- **Educational Focus**: Clear structure demonstrating fundamental data structure operations
- **Minimal Complexity**: Streamlined implementations without unnecessary overhead
- **Complete Functionality**: All essential operations for each data structure

## Practical Applications

- **Stacks**: Function call management, expression evaluation, undo operations
- **Queues**: Task scheduling, breadth-first search, printer queues
- **Linked Lists**: Dynamic memory allocation, implementation of other data structures
- **Trees**: File systems, decision trees, organizational hierarchies
