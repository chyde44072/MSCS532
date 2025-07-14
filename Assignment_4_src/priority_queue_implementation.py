"""
This module implements a binary heap-based priority queue with task scheduling
applications. Supports both max-heap and min-heap operations.
"""

import time
from typing import List, Optional, Any
from dataclasses import dataclass


@dataclass
class Task:
    """
    Represents a task with priority, timing, and metadata.
    """
    task_id: int
    priority: int
    arrival_time: float
    deadline: float
    description: str = ""
    
    def __lt__(self, other):
        """For min-heap comparison based on priority."""
        return self.priority < other.priority
    
    def __gt__(self, other):
        """For max-heap comparison based on priority."""
        return self.priority > other.priority
    
    def __eq__(self, other):
        """Equality comparison based on task_id."""
        return self.task_id == other.task_id
    
    def __repr__(self):
        return f"Task(id={self.task_id}, priority={self.priority}, arrival={self.arrival_time}, deadline={self.deadline})"


class PriorityQueue:
    """
    Binary heap-based priority queue implementation.
    
    Supports both max-heap (highest priority first) and min-heap (lowest priority first).
    """
    
    def __init__(self, max_heap: bool = True):
        """
        Initialize the priority queue.
        
        Args:
            max_heap: If True, use max-heap (highest priority first).
                     If False, use min-heap (lowest priority first).
        """
        self.heap: List[Task] = []
        self.max_heap = max_heap
        self.task_positions = {}  # Map task_id to heap index for O(1) lookup
    
    def _parent(self, index: int) -> int:
        """Get parent index."""
        return (index - 1) // 2
    
    def _left_child(self, index: int) -> int:
        """Get left child index."""
        return 2 * index + 1
    
    def _right_child(self, index: int) -> int:
        """Get right child index."""
        return 2 * index + 2
    
    def _compare(self, task1: Task, task2: Task) -> bool:
        """
        Compare two tasks based on heap type.
        
        Returns:
            True if task1 should be higher in the heap than task2
        """
        if self.max_heap:
            return task1.priority > task2.priority
        else:
            return task1.priority < task2.priority
    
    def _swap(self, i: int, j: int) -> None:
        """Swap two elements in the heap and update position tracking."""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        # Update position tracking
        self.task_positions[self.heap[i].task_id] = i
        self.task_positions[self.heap[j].task_id] = j
    
    def _heapify_up(self, index: int) -> None:
        """
        Restore heap property by moving element up.
        
        Args:
            index: Index of the element to heapify up
        """
        while index > 0:
            parent_index = self._parent(index)
            if self._compare(self.heap[index], self.heap[parent_index]):
                self._swap(index, parent_index)
                index = parent_index
            else:
                break
    
    def _heapify_down(self, index: int) -> None:
        """
        Restore heap property by moving element down.
        
        Args:
            index: Index of the element to heapify down
        """
        while True:
            largest_or_smallest = index
            left = self._left_child(index)
            right = self._right_child(index)
            
            # Find the element that should be at the root
            if (left < len(self.heap) and 
                self._compare(self.heap[left], self.heap[largest_or_smallest])):
                largest_or_smallest = left
            
            if (right < len(self.heap) and 
                self._compare(self.heap[right], self.heap[largest_or_smallest])):
                largest_or_smallest = right
            
            if largest_or_smallest != index:
                self._swap(index, largest_or_smallest)
                index = largest_or_smallest
            else:
                break
    
    def insert(self, task: Task) -> None:
        """
        Insert a new task into the priority queue.
        
        Time Complexity: O(log n)
        
        Args:
            task: The task to insert
        """
        self.heap.append(task)
        task_index = len(self.heap) - 1
        self.task_positions[task.task_id] = task_index
        self._heapify_up(task_index)
    
    def extract_max(self) -> Optional[Task]:
        """
        Remove and return the task with highest priority (max-heap).
        
        Time Complexity: O(log n)
        
        Returns:
            The task with highest priority, or None if queue is empty
        """
        if not self.max_heap:
            raise ValueError("extract_max() called on min-heap. Use extract_min() instead.")
        
        return self._extract_root()
    
    def extract_min(self) -> Optional[Task]:
        """
        Remove and return the task with lowest priority (min-heap).
        
        Time Complexity: O(log n)
        
        Returns:
            The task with lowest priority, or None if queue is empty
        """
        if self.max_heap:
            raise ValueError("extract_min() called on max-heap. Use extract_max() instead.")
        
        return self._extract_root()
    
    def _extract_root(self) -> Optional[Task]:
        """Internal method to extract the root element."""
        if not self.heap:
            return None
        
        if len(self.heap) == 1:
            task = self.heap.pop()
            del self.task_positions[task.task_id]
            return task
        
        # Store the root task to return
        root_task = self.heap[0]
        
        # Move last element to root and remove it from the end
        last_task = self.heap.pop()
        self.heap[0] = last_task
        
        # Update position tracking
        del self.task_positions[root_task.task_id]
        self.task_positions[last_task.task_id] = 0
        
        # Restore heap property
        self._heapify_down(0)
        
        return root_task
    
    def increase_key(self, task_id: int, new_priority: int) -> bool:
        """
        Increase the priority of a task (for max-heap).
        
        Time Complexity: O(log n)
        
        Args:
            task_id: ID of the task to modify
            new_priority: New priority value (should be higher)
            
        Returns:
            True if operation was successful, False otherwise
        """
        if not self.max_heap:
            raise ValueError("increase_key() called on min-heap. Use decrease_key() instead.")
        
        if task_id not in self.task_positions:
            return False
        
        index = self.task_positions[task_id]
        old_priority = self.heap[index].priority
        
        if new_priority <= old_priority:
            return False  # New priority must be higher
        
        self.heap[index].priority = new_priority
        self._heapify_up(index)
        return True
    
    def decrease_key(self, task_id: int, new_priority: int) -> bool:
        """
        Decrease the priority of a task (for min-heap).
        
        Time Complexity: O(log n)
        
        Args:
            task_id: ID of the task to modify
            new_priority: New priority value (should be lower)
            
        Returns:
            True if operation was successful, False otherwise
        """
        if self.max_heap:
            raise ValueError("decrease_key() called on max-heap. Use increase_key() instead.")
        
        if task_id not in self.task_positions:
            return False
        
        index = self.task_positions[task_id]
        old_priority = self.heap[index].priority
        
        if new_priority >= old_priority:
            return False  # New priority must be lower
        
        self.heap[index].priority = new_priority
        self._heapify_up(index)
        return True
    
    def peek(self) -> Optional[Task]:
        """
        Return the highest/lowest priority task without removing it.
        
        Time Complexity: O(1)
        
        Returns:
            The root task, or None if queue is empty
        """
        return self.heap[0] if self.heap else None
    
    def is_empty(self) -> bool:
        """
        Check if the priority queue is empty.
        
        Time Complexity: O(1)
        
        Returns:
            True if queue is empty, False otherwise
        """
        return len(self.heap) == 0
    
    def size(self) -> int:
        """
        Get the number of tasks in the queue.
        
        Time Complexity: O(1)
        
        Returns:
            Number of tasks in the queue
        """
        return len(self.heap)
    
    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID.
        
        Time Complexity: O(1)
        
        Args:
            task_id: ID of the task to retrieve
            
        Returns:
            The task if found, None otherwise
        """
        if task_id not in self.task_positions:
            return None
        
        index = self.task_positions[task_id]
        return self.heap[index]
    
    def __str__(self) -> str:
        """String representation of the priority queue."""
        if not self.heap:
            return "PriorityQueue(empty)"
        
        heap_type = "max-heap" if self.max_heap else "min-heap"
        return f"PriorityQueue({heap_type}, size={len(self.heap)}, root={self.heap[0]})"
    
    def __len__(self) -> int:
        """Return the size of the priority queue."""
        return len(self.heap)


def demonstrate_priority_queue():
    """
    Demonstrate the functionality of the priority queue.
    """
    print("=" * 60)
    print("PRIORITY QUEUE DEMONSTRATION")
    print("=" * 60)
    
    # Test max-heap
    print("\n1. Max-Heap Priority Queue (Highest Priority First):")
    max_pq = PriorityQueue(max_heap=True)
    
    # Create test tasks
    tasks = [
        Task(1, 5, 0.0, 10.0, "High priority task"),
        Task(2, 2, 1.0, 15.0, "Low priority task"),
        Task(3, 8, 2.0, 5.0, "Critical task"),
        Task(4, 3, 3.0, 12.0, "Medium priority task"),
        Task(5, 7, 4.0, 8.0, "Important task")
    ]
    
    print("Inserting tasks:")
    for task in tasks:
        max_pq.insert(task)
        print(f"  Inserted: {task}")
    
    print(f"\nQueue state: {max_pq}")
    print(f"Root (highest priority): {max_pq.peek()}")
    
    print("\nExtracting tasks in priority order:")
    while not max_pq.is_empty():
        task = max_pq.extract_max()
        print(f"  Extracted: {task}")
    
    # Test min-heap
    print("\n2. Min-Heap Priority Queue (Lowest Priority First):")
    min_pq = PriorityQueue(max_heap=False)
    
    for task in tasks:
        min_pq.insert(task)
    
    print(f"Root (lowest priority): {min_pq.peek()}")
    
    print("\nExtracting tasks in priority order:")
    while not min_pq.is_empty():
        task = min_pq.extract_min()
        print(f"  Extracted: {task}")
    
    # Test priority modification
    print("\n3. Priority Modification:")
    pq = PriorityQueue(max_heap=True)
    
    test_task = Task(100, 5, 0.0, 10.0, "Test task")
    pq.insert(test_task)
    print(f"Original task: {test_task}")
    
    # Increase priority
    success = pq.increase_key(100, 9)
    print(f"Increased priority to 9: {success}")
    print(f"Updated task: {pq.get_task_by_id(100)}")


def analyze_priority_queue_performance():
    """
    Analyze the performance characteristics of priority queue operations.
    """
    print("\n4. Performance Analysis:")
    print("-" * 40)
    
    sizes = [100, 500, 1000, 5000, 10000]
    
    for size in sizes:
        print(f"\nTesting with {size} elements:")
        
        # Create priority queue
        pq = PriorityQueue(max_heap=True)
        
        # Measure insertion time
        start_time = time.time()
        for i in range(size):
            task = Task(i, i, 0.0, 10.0, f"Task {i}")
            pq.insert(task)
        insert_time = time.time() - start_time
        
        # Measure extraction time
        start_time = time.time()
        while not pq.is_empty():
            pq.extract_max()
        extract_time = time.time() - start_time
        
        print(f"  Insert {size} elements: {insert_time:.4f}s")
        print(f"  Extract {size} elements: {extract_time:.4f}s")
        print(f"  Average insert time: {insert_time/size*1000:.4f}ms")
        print(f"  Average extract time: {extract_time/size*1000:.4f}ms")


if __name__ == "__main__":
    # Run demonstrations
    demonstrate_priority_queue()
    analyze_priority_queue_performance()
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE!")
    print("=" * 60)
