"""
This module simulates a task scheduling system using the priority queue
implementation to demonstrate real-world applications.
"""

import random
import time
from typing import List, Dict, Tuple
from priority_queue_implementation import PriorityQueue, Task


class TaskScheduler:
    """
    Task scheduler that uses a priority queue to manage task execution.
    """
    
    def __init__(self, max_heap: bool = True):
        """
        Initialize the task scheduler.
        
        Args:
            max_heap: If True, higher priority tasks are executed first
        """
        self.queue = PriorityQueue(max_heap=max_heap)
        self.completed_tasks = []
        self.current_time = 0.0
        self.max_heap = max_heap
    
    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler."""
        self.queue.insert(task)
        print(f"Added task: {task}")
    
    def execute_next_task(self) -> bool:
        """
        Execute the next highest priority task.
        
        Returns:
            True if a task was executed, False if queue is empty
        """
        if self.queue.is_empty():
            return False
        
        if self.max_heap:
            task = self.queue.extract_max()
        else:
            task = self.queue.extract_min()
        
        execution_time = random.uniform(0.5, 2.0)  # Simulate execution time
        self.current_time += execution_time
        
        task.completion_time = self.current_time
        self.completed_tasks.append(task)
        
        print(f"Executed task: {task} (took {execution_time:.2f}s)")
        return True
    
    def simulate_scheduling(self, tasks: List[Task]) -> Dict:
        """
        Simulate the complete scheduling process.
        
        Args:
            tasks: List of tasks to schedule
            
        Returns:
            Dictionary with simulation results
        """
        print("=" * 60)
        print("TASK SCHEDULING SIMULATION")
        print("=" * 60)
        
        # Add all tasks to the scheduler
        for task in tasks:
            self.add_task(task)
        
        print(f"\nStarting execution with {len(tasks)} tasks...")
        print("-" * 40)
        
        # Execute all tasks
        while self.execute_next_task():
            pass
        
        # Calculate performance metrics
        total_completion_time = self.current_time
        average_waiting_time = self._calculate_average_waiting_time()
        missed_deadlines = self._count_missed_deadlines()
        
        results = {
            'total_completion_time': total_completion_time,
            'average_waiting_time': average_waiting_time,
            'missed_deadlines': missed_deadlines,
            'completed_tasks': len(self.completed_tasks)
        }
        
        print("-" * 40)
        print("SIMULATION RESULTS:")
        print(f"Total completion time: {total_completion_time:.2f}s")
        print(f"Average waiting time: {average_waiting_time:.2f}s")
        print(f"Missed deadlines: {missed_deadlines}")
        print(f"Completed tasks: {len(self.completed_tasks)}")
        
        return results
    
    def _calculate_average_waiting_time(self) -> float:
        """Calculate the average waiting time for all tasks."""
        if not self.completed_tasks:
            return 0.0
        
        total_waiting_time = 0.0
        for task in self.completed_tasks:
            waiting_time = task.completion_time - task.arrival_time
            total_waiting_time += waiting_time
        
        return total_waiting_time / len(self.completed_tasks)
    
    def _count_missed_deadlines(self) -> int:
        """Count the number of tasks that missed their deadlines."""
        missed = 0
        for task in self.completed_tasks:
            if task.completion_time > task.deadline:
                missed += 1
        return missed
    
    def get_task_statistics(self) -> Dict:
        """Get detailed statistics about task execution."""
        if not self.completed_tasks:
            return {}
        
        priorities = [task.priority for task in self.completed_tasks]
        waiting_times = [task.completion_time - task.arrival_time for task in self.completed_tasks]
        
        return {
            'min_priority': min(priorities),
            'max_priority': max(priorities),
            'avg_priority': sum(priorities) / len(priorities),
            'min_waiting_time': min(waiting_times),
            'max_waiting_time': max(waiting_times),
            'avg_waiting_time': sum(waiting_times) / len(waiting_times)
        }


def generate_random_tasks(num_tasks: int) -> List[Task]:
    """
    Generate a list of random tasks for simulation.
    
    Args:
        num_tasks: Number of tasks to generate
        
    Returns:
        List of randomly generated tasks
    """
    tasks = []
    for i in range(num_tasks):
        task = Task(
            task_id=i,
            priority=random.randint(1, 10),
            arrival_time=random.uniform(0, 5),
            deadline=random.uniform(5, 20),
            description=f"Random task {i}"
        )
        tasks.append(task)
    
    return tasks


def create_realistic_task_scenario() -> List[Task]:
    """
    Create a realistic task scenario with different types of tasks.
    
    Returns:
        List of tasks representing a realistic workload
    """
    tasks = [
        # Critical system tasks
        Task(1, 10, 0.0, 2.0, "System boot initialization"),
        Task(2, 9, 0.5, 3.0, "Security scan"),
        Task(3, 8, 1.0, 4.0, "Database backup"),
        
        # High priority user tasks
        Task(4, 7, 1.5, 8.0, "User login request"),
        Task(5, 6, 2.0, 10.0, "File upload processing"),
        Task(6, 7, 2.5, 6.0, "Email sending"),
        
        # Medium priority tasks
        Task(7, 5, 3.0, 12.0, "Report generation"),
        Task(8, 4, 3.5, 15.0, "Data analytics"),
        Task(9, 5, 4.0, 14.0, "Cache cleanup"),
        
        # Low priority maintenance tasks
        Task(10, 3, 4.5, 20.0, "Log rotation"),
        Task(11, 2, 5.0, 25.0, "System optimization"),
        Task(12, 1, 5.5, 30.0, "Archive old data")
    ]
    
    return tasks


def compare_scheduling_strategies():
    """
    Compare max-heap vs min-heap scheduling strategies.
    """
    print("\n" + "=" * 60)
    print("COMPARING SCHEDULING STRATEGIES")
    print("=" * 60)
    
    # Create test tasks
    tasks = create_realistic_task_scenario()
    
    # Test max-heap scheduling (highest priority first)
    print("\n1. MAX-HEAP SCHEDULING (Highest Priority First):")
    max_scheduler = TaskScheduler(max_heap=True)
    max_results = max_scheduler.simulate_scheduling(tasks.copy())
    max_stats = max_scheduler.get_task_statistics()
    
    # Test min-heap scheduling (lowest priority first)
    print("\n2. MIN-HEAP SCHEDULING (Lowest Priority First):")
    min_scheduler = TaskScheduler(max_heap=False)
    min_results = min_scheduler.simulate_scheduling(tasks.copy())
    min_stats = min_scheduler.get_task_statistics()
    
    # Compare results
    print("\n3. COMPARISON:")
    print("-" * 40)
    print(f"{'Metric':<25} {'Max-Heap':<15} {'Min-Heap':<15}")
    print("-" * 40)
    print(f"{'Total time':<25} {max_results['total_completion_time']:<15.2f} {min_results['total_completion_time']:<15.2f}")
    print(f"{'Avg waiting time':<25} {max_results['average_waiting_time']:<15.2f} {min_results['average_waiting_time']:<15.2f}")
    print(f"{'Missed deadlines':<25} {max_results['missed_deadlines']:<15} {min_results['missed_deadlines']:<15}")
    
    return max_results, min_results


def stress_test_scheduler():
    """
    Perform stress testing on the scheduler with large numbers of tasks.
    """
    print("\n" + "=" * 60)
    print("SCHEDULER STRESS TEST")
    print("=" * 60)
    
    test_sizes = [100, 500, 1000, 2000]
    
    for size in test_sizes:
        print(f"\nTesting with {size} tasks:")
        
        # Generate random tasks
        tasks = generate_random_tasks(size)
        
        # Measure scheduling time
        scheduler = TaskScheduler(max_heap=True)
        start_time = time.time()
        
        # Add all tasks
        for task in tasks:
            scheduler.queue.insert(task)
        
        # Execute all tasks (without printing)
        while not scheduler.queue.is_empty():
            task = scheduler.queue.extract_max()
            scheduler.completed_tasks.append(task)
        
        total_time = time.time() - start_time
        
        print(f"  Total scheduling time: {total_time:.4f}s")
        print(f"  Average time per task: {total_time/size*1000:.4f}ms")
        print(f"  Tasks processed: {len(scheduler.completed_tasks)}")


def demonstrate_key_operations():
    """
    Demonstrate key priority queue operations in scheduling context.
    """
    print("\n" + "=" * 60)
    print("PRIORITY QUEUE OPERATIONS DEMONSTRATION")
    print("=" * 60)
    
    scheduler = TaskScheduler(max_heap=True)
    
    # Add initial tasks
    tasks = [
        Task(1, 5, 0.0, 10.0, "Medium priority task"),
        Task(2, 3, 1.0, 15.0, "Low priority task"),
        Task(3, 7, 2.0, 8.0, "High priority task")
    ]
    
    for task in tasks:
        scheduler.add_task(task)
    
    print(f"\nCurrent queue state: {scheduler.queue}")
    print(f"Next task to execute: {scheduler.queue.peek()}")
    
    # Demonstrate priority increase
    print("\n1. Increasing priority of task 2 from 3 to 8:")
    success = scheduler.queue.increase_key(2, 8)
    print(f"Operation successful: {success}")
    print(f"Updated queue state: {scheduler.queue}")
    print(f"New next task: {scheduler.queue.peek()}")
    
    # Execute tasks
    print("\n2. Executing tasks in priority order:")
    while not scheduler.queue.is_empty():
        task = scheduler.queue.extract_max()
        print(f"  Executed: {task}")


if __name__ == "__main__":
    # Run all demonstrations
    demonstrate_key_operations()
    compare_scheduling_strategies()
    stress_test_scheduler()
    
    print("\n" + "=" * 60)
    print("TASK SCHEDULER SIMULATION COMPLETE!")
    print("=" * 60)
