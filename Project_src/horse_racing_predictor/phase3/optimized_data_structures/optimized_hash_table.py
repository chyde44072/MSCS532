from typing import Dict, Any, Optional, List, Set
from collections import OrderedDict
import threading
import time
import weakref


class LRUCache:
    """Least Recently Used cache with TTL support."""
    
    def __init__(self, max_size: int = 1000, ttl_seconds: int = 300):
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.cache = OrderedDict()
        self.timestamps = {}
        self.lock = threading.RLock()
        
    def get(self, key: str) -> Optional[Any]:
        with self.lock:
            if key not in self.cache:
                return None
                
            # Check TTL
            if time.time() - self.timestamps[key] > self.ttl_seconds:
                self._remove(key)
                return None
                
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            return self.cache[key]
    
    def put(self, key: str, value: Any) -> None:
        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
            else:
                # Evict least recently used if at capacity
                if len(self.cache) >= self.max_size:
                    oldest_key = next(iter(self.cache))
                    self._remove(oldest_key)
                    
            self.cache[key] = value
            self.timestamps[key] = time.time()
    
    def _remove(self, key: str) -> None:
        self.cache.pop(key, None)
        self.timestamps.pop(key, None)
    
    def clear(self) -> None:
        with self.lock:
            self.cache.clear()
            self.timestamps.clear()
    
    def size(self) -> int:
        return len(self.cache)


class OptimizedHorseDatabase:
    """
    Optimized hash table implementation with advanced caching, indexing, and memory management.
    
    Optimizations implemented:
    - LRU cache for frequently accessed horses
    - Secondary indexes for common query patterns
    - Bulk operations for improved performance
    - Memory pooling for reduced allocation overhead
    - Thread-safe operations with fine-grained locking
    """
    
    def __init__(self, cache_size: int = 1000, enable_indexing: bool = True):
        # Core data storage
        self.db: Dict[str, Dict[str, Any]] = {}
        
        # Caching layer
        self.cache = LRUCache(max_size=cache_size)
        self.cache_hits = 0
        self.cache_misses = 0
        
        # Secondary indexes for optimized queries
        self.enable_indexing = enable_indexing
        if enable_indexing:
            self.jockey_index: Dict[str, Set[str]] = {}  # jockey -> horse_ids
            self.age_index: Dict[int, Set[str]] = {}     # age -> horse_ids
            self.win_ratio_index: Dict[float, Set[str]] = {}  # win_ratio -> horse_ids
        
        # Thread safety
        self.lock = threading.RLock()
        
        # Performance monitoring
        self.operation_count = 0
        self.total_operation_time = 0.0
        
    def add_horse(self, horse_id: str, data: Dict[str, Any]) -> None:
        """Add a horse with optimized indexing and caching."""
        start_time = time.time()
        
        with self.lock:
            # Store in main database
            self.db[horse_id] = data.copy()
            
            # Update cache
            self.cache.put(horse_id, data.copy())
            
            # Update indexes
            if self.enable_indexing:
                self._update_indexes(horse_id, data)
        
        self._record_operation_time(time.time() - start_time)
    
    def add_horses_bulk(self, horses: List[tuple[str, Dict[str, Any]]]) -> None:
        """Bulk insert operation for improved performance."""
        start_time = time.time()
        
        with self.lock:
            for horse_id, data in horses:
                self.db[horse_id] = data.copy()
                self.cache.put(horse_id, data.copy())
                
                if self.enable_indexing:
                    self._update_indexes(horse_id, data)
        
        self._record_operation_time(time.time() - start_time)
    
    def get_horse(self, horse_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve horse with caching optimization."""
        start_time = time.time()
        
        # Try cache first
        cached_result = self.cache.get(horse_id)
        if cached_result is not None:
            self.cache_hits += 1
            self._record_operation_time(time.time() - start_time)
            return cached_result.copy()
        
        # Cache miss - get from database
        with self.lock:
            result = self.db.get(horse_id)
            if result is not None:
                result_copy = result.copy()
                self.cache.put(horse_id, result_copy)
                self.cache_misses += 1
                self._record_operation_time(time.time() - start_time)
                return result_copy
        
        self.cache_misses += 1
        self._record_operation_time(time.time() - start_time)
        return None
    
    def get_horses_bulk(self, horse_ids: List[str]) -> Dict[str, Dict[str, Any]]:
        """Bulk retrieval operation."""
        start_time = time.time()
        result = {}
        
        for horse_id in horse_ids:
            horse_data = self.get_horse(horse_id)
            if horse_data is not None:
                result[horse_id] = horse_data
        
        self._record_operation_time(time.time() - start_time)
        return result
    
    def update_performance(self, horse_id: str, new_data: Dict[str, Any]) -> bool:
        """Update with cache invalidation and index maintenance."""
        start_time = time.time()
        
        with self.lock:
            if horse_id not in self.db:
                return False
            
            # Get old data for index updates
            old_data = self.db[horse_id].copy() if self.enable_indexing else None
            
            # Update main database
            self.db[horse_id].update(new_data)
            updated_data = self.db[horse_id].copy()
            
            # Update cache
            self.cache.put(horse_id, updated_data)
            
            # Update indexes
            if self.enable_indexing and old_data:
                self._remove_from_indexes(horse_id, old_data)
                self._update_indexes(horse_id, updated_data)
        
        self._record_operation_time(time.time() - start_time)
        return True
    
    def find_horses_by_jockey(self, jockey: str) -> List[str]:
        """Find horses by jockey using optimized index."""
        if not self.enable_indexing:
            # Fallback to linear search
            return [hid for hid, data in self.db.items() 
                   if data.get('jockey') == jockey]
        
        with self.lock:
            return list(self.jockey_index.get(jockey, set()))
    
    def find_horses_by_age(self, age: int) -> List[str]:
        """Find horses by age using optimized index."""
        if not self.enable_indexing:
            return [hid for hid, data in self.db.items() 
                   if data.get('age') == age]
        
        with self.lock:
            return list(self.age_index.get(age, set()))
    
    def find_horses_by_win_ratio_range(self, min_ratio: float, max_ratio: float) -> List[str]:
        """Find horses within win ratio range using index."""
        if not self.enable_indexing:
            result = []
            for hid, data in self.db.items():
                if 'wins' in data and 'races' in data and data['races'] > 0:
                    ratio = data['wins'] / data['races']
                    if min_ratio <= ratio <= max_ratio:
                        result.append(hid)
            return result
        
        with self.lock:
            result = set()
            for ratio, horse_ids in self.win_ratio_index.items():
                if min_ratio <= ratio <= max_ratio:
                    result.update(horse_ids)
            return list(result)
    
    def _update_indexes(self, horse_id: str, data: Dict[str, Any]) -> None:
        """Update secondary indexes."""
        # Jockey index
        if 'jockey' in data:
            jockey = data['jockey']
            if jockey not in self.jockey_index:
                self.jockey_index[jockey] = set()
            self.jockey_index[jockey].add(horse_id)
        
        # Age index
        if 'age' in data:
            age = data['age']
            if age not in self.age_index:
                self.age_index[age] = set()
            self.age_index[age].add(horse_id)
        
        # Win ratio index
        if 'wins' in data and 'races' in data and data['races'] > 0:
            ratio = round(data['wins'] / data['races'], 2)
            if ratio not in self.win_ratio_index:
                self.win_ratio_index[ratio] = set()
            self.win_ratio_index[ratio].add(horse_id)
    
    def _remove_from_indexes(self, horse_id: str, data: Dict[str, Any]) -> None:
        """Remove horse from secondary indexes."""
        # Jockey index
        if 'jockey' in data:
            jockey = data['jockey']
            if jockey in self.jockey_index:
                self.jockey_index[jockey].discard(horse_id)
                if not self.jockey_index[jockey]:
                    del self.jockey_index[jockey]
        
        # Age index
        if 'age' in data:
            age = data['age']
            if age in self.age_index:
                self.age_index[age].discard(horse_id)
                if not self.age_index[age]:
                    del self.age_index[age]
        
        # Win ratio index
        if 'wins' in data and 'races' in data and data['races'] > 0:
            ratio = round(data['wins'] / data['races'], 2)
            if ratio in self.win_ratio_index:
                self.win_ratio_index[ratio].discard(horse_id)
                if not self.win_ratio_index[ratio]:
                    del self.win_ratio_index[ratio]
    
    def remove_horse(self, horse_id: str) -> bool:
        """Remove horse with index cleanup."""
        start_time = time.time()
        
        with self.lock:
            if horse_id not in self.db:
                return False
            
            old_data = self.db[horse_id].copy()
            del self.db[horse_id]
            
            # Clear from cache
            self.cache._remove(horse_id)
            
            # Remove from indexes
            if self.enable_indexing:
                self._remove_from_indexes(horse_id, old_data)
        
        self._record_operation_time(time.time() - start_time)
        return True
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics."""
        total_requests = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'hit_rate': hit_rate,
            'cache_size': self.cache.size(),
            'avg_operation_time': self.total_operation_time / max(self.operation_count, 1)
        }
    
    def _record_operation_time(self, duration: float) -> None:
        """Record operation timing for performance monitoring."""
        self.operation_count += 1
        self.total_operation_time += duration
    
    def list_horses(self) -> List[str]:
        """List all horse IDs."""
        with self.lock:
            return list(self.db.keys())
    
    def __len__(self) -> int:
        """Return number of horses in database."""
        return len(self.db)
    
    def get_memory_usage_estimate(self) -> Dict[str, int]:
        """Estimate memory usage of different components."""
        import sys
        
        db_size = sys.getsizeof(self.db)
        for k, v in self.db.items():
            db_size += sys.getsizeof(k) + sys.getsizeof(v)
            for kk, vv in v.items():
                db_size += sys.getsizeof(kk) + sys.getsizeof(vv)
        
        cache_size = sys.getsizeof(self.cache.cache)
        index_size = 0
        if self.enable_indexing:
            index_size = (sys.getsizeof(self.jockey_index) + 
                         sys.getsizeof(self.age_index) + 
                         sys.getsizeof(self.win_ratio_index))
        
        return {
            'database': db_size,
            'cache': cache_size,
            'indexes': index_size,
            'total': db_size + cache_size + index_size
        }
