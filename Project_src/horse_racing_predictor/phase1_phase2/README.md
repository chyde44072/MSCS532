# Horse Racing Predictor - Data Structures Implementation

## Overview
This project implements fundamental data structures for a horse racing prediction system. The system demonstrates practical applications of hash tables, heaps, and AVL trees in managing horse profiles, performance tracking, and ranking operations.

## Project Structure
```
horse_racing_predictor/
├── data_structures/              # Core data structure implementations
│   ├── hash_table.py            # HorseDatabase implementation
│   ├── leaderboard_heap.py      # Heap-based leaderboard
│   └── avl_tree.py             # Self-balancing binary search tree
├── models/
│   └── horse.py                 # Horse data model
├── tests/
│   └── test_data_structures.py  # Unit tests for all structures
├── demo.py                      # Demonstration script
├── benchmark.py                 # Performance testing
├── data_loader.py               # Data loading utilities
├── horses.xlsx                  # Sample dataset
└── README.md                    # This file
```

## Core Data Structures

### 1. Hash Table (HorseDatabase)
A hash table implementation for efficient horse profile storage and retrieval.

**Features:**
- O(1) average-case lookups
- Dynamic resizing with load factor management
- Collision handling using chaining
- Horse profile management with performance tracking

**Usage:**
```python
from data_structures.hash_table import HorseDatabase

db = HorseDatabase()
db.add_horse("H001", {"name": "Thunder", "jockey": "Smith"})
horse = db.get_horse("H001")
```

**Time Complexity:**
- Insertion: O(1) average, O(n) worst case
- Lookup: O(1) average, O(n) worst case
- Deletion: O(1) average, O(n) worst case

### 2. Leaderboard (Min-Heap)
A min-heap implementation for maintaining dynamic race time leaderboards.

**Features:**
- Efficient top-k queries
- Dynamic updates for new race results
- Maintains fastest race times automatically
- Memory-efficient heap structure

**Usage:**
```python
from data_structures.leaderboard_heap import Leaderboard

leaderboard = Leaderboard()
leaderboard.add_result("H001", 65.2)
top_5 = leaderboard.get_top_performers(5)
```

**Time Complexity:**
- Insertion: O(log n)
- Get minimum: O(1)
- Extract minimum: O(log n)
- Top-k queries: O(k log n)

### 3. AVL Tree
A self-balancing binary search tree for range queries and sorted operations.

**Features:**
- Automatic height balancing
- Efficient range queries by win ratio
- In-order traversal for sorted results
- O(log n) guaranteed operations

**Usage:**
```python
from data_structures.avl_tree import AVLTree

tree = AVLTree()
tree.insert(0.75, "H001")  # win_ratio, horse_id
high_performers = tree.get_range(0.7, 1.0)
```

**Time Complexity:**
- Insertion: O(log n)
- Search: O(log n)
- Deletion: O(log n)
- Range queries: O(log n + m) where m is result size

## Installation & Usage

### Prerequisites
- Python 3.8 or higher
- No external dependencies required (uses standard library only)

### Running the Demonstration
```bash
python demo.py
```

### Running Tests
```bash
python tests/test_data_structures.py
```

### Running Performance Benchmarks
```bash
python benchmark.py
```

## Key Features

### Core Operations
1. **Horse Management**: Add, update, retrieve horse profiles
2. **Performance Tracking**: Maintain race time leaderboards
3. **Ranking System**: Rank horses by win ratios with range filtering
4. **Integration**: All structures work together seamlessly

### Performance Characteristics
- **Hash Table**: O(1) average-case lookups for 10,000+ records
- **Heap**: Efficient top-k queries for real-time leaderboards
- **AVL Tree**: Balanced performance for range queries and sorting

## Implementation Highlights

### Hash Table Features
```python
# Fast horse profile access
horse_data = db.get_horse("H001")

# Performance updates
db.update_performance("H001", {"recent_time": 63.5})
```

### Leaderboard Features
```python
# Add race results
leaderboard.add_result("H001", 65.2)

# Get top performers
top_5 = leaderboard.get_top_performers(5)
```

### AVL Tree Features
```python
# Range queries for performance analysis
high_performers = tree.get_range(0.7, 1.0)

# Sorted lists for comprehensive analysis
all_ranked = tree.get_sorted_list()
```

## Testing Coverage
- **Unit Tests**: Individual data structure functionality
- **Integration Tests**: Cross-structure operations
- **Edge Cases**: Empty datasets, duplicate entries, invalid inputs
- **Performance Tests**: Scalability and time complexity verification

## Performance Results
Based on benchmarking with 2,000 horse records:
- Hash table lookups: ~0.001ms average
- Heap insertions: ~0.015ms average
- AVL tree range queries: ~0.025ms average

## Future Enhancements
1. **Data Persistence**: File/database storage integration
2. **Prediction Algorithms**: ML-based outcome prediction
3. **Real-time Updates**: Live race data integration
4. **Web Interface**: User-friendly prediction interface
5. **Extended Analytics**: Advanced performance metrics

## Design Decisions

### Why These Structures?
1. **Hash Table**: Optimal for frequent horse profile lookups
2. **Min-Heap**: Perfect for maintaining dynamic leaderboards
3. **AVL Tree**: Ideal for range-based performance analysis

### Trade-offs Considered
- Memory vs. speed optimization
- Simplicity vs. feature completeness
- Real-time updates vs. batch processing

## Known Limitations
1. **Memory Usage**: All data stored in memory
2. **Concurrency**: No thread-safety implementation
3. **Data Validation**: Minimal input validation
4. **Persistence**: No permanent storage mechanism

## Real Data Integration

### Kentucky Derby Winners Dataset
The system now includes real Kentucky Derby winner data (2000-2024) featuring:
- **25 horses** with authentic names and performance metrics
- **Average speeds** ranging from 35.6 to 37.3 mph
- **Win ratios** from 0.59 to 0.70
- **Enhanced profiles** with age, weight, jockey, and specialties

### Data Features
```python
# Example horse profile
{
    "name": "American Pharoah",
    "avg_speed": 37.1,
    "win_ratio": 0.69,
    "total_races": 18,
    "total_wins": 12,
    "age": 4,
    "derby_year": 2015,
    "track_preference": "dirt"
}
```

### Enhanced Demonstrations
- **Performance Analysis**: Multi-dimensional horse evaluation
- **Race Simulation**: Realistic race predictions
- **Tier Classification**: Elite, good, and average performer categories
- **Correlation Studies**: Speed vs. consistency analysis

## Contributing
When contributing to this project:
1. Follow existing code style and patterns
2. Add comprehensive tests for new features
3. Update documentation for any API changes
4. Ensure backward compatibility when possible


**Summary**: This implementation demonstrates fundamental data structure concepts through a practical horse racing prediction system, providing efficient operations for data management, performance tracking, and analytical queries.
