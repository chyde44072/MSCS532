import heapq
from typing import List, Tuple, Dict, Optional, Set
import threading
import time
from collections import defaultdict
import bisect


class OptimizedLeaderboard:
    def __init__(self, cache_top_k: int = 20, enable_range_queries: bool = True):
        # Core heap data structure
        self.heap: List[Tuple[float, str]] = []
        self.entries: Set[str] = set()
        self.horse_times: Dict[str, float] = {}
        
        # Caching layer
        self.cache_top_k = cache_top_k
        self.cached_top_results: Optional[List[Tuple[float, str]]] = None
        self.cache_valid = False
        
        # Range query optimization
        self.enable_range_queries = enable_range_queries
        if enable_range_queries:
            self.sorted_times: List[Tuple[float, str]] = []
            self.sorted_valid = False
        
        # Performance tracking
        self.update_count = 0
        self.query_count = 0
        self.cache_hits = 0
        self.cache_misses = 0
        
        # Thread safety
        self.lock = threading.RLock()
        
        # Bulk operation support
        self.pending_updates: List[Tuple[str, float]] = []
        self.batch_size = 100
    
    def add_result(self, horse_id: str, race_time: float) -> None:
        """Add a single race result with optimized caching."""
        with self.lock:
            self._add_result_internal(horse_id, race_time)
            self._invalidate_caches()
    
    def add_results_bulk(self, results: List[Tuple[str, float]]) -> None:
        """Bulk add operation for improved performance."""
        start_time = time.time()
        
        with self.lock:
            # Process in batches to manage memory
            for i in range(0, len(results), self.batch_size):
                batch = results[i:i + self.batch_size]
                for horse_id, race_time in batch:
                    self._add_result_internal(horse_id, race_time)
            
            self._invalidate_caches()
            self.update_count += len(results)
    
    def _add_result_internal(self, horse_id: str, race_time: float) -> None:
        """Internal method for adding results without cache invalidation."""
        if horse_id not in self.entries:
            heapq.heappush(self.heap, (race_time, horse_id))
            self.entries.add(horse_id)
            self.horse_times[horse_id] = race_time
        else:
            # Update if this is a better (lower) time
            if race_time < self.horse_times[horse_id]:
                self.horse_times[horse_id] = race_time
                # Mark for heap rebuild instead of immediate rebuild
                self._mark_heap_dirty()
    
    def _mark_heap_dirty(self) -> None:
        """Mark heap as needing rebuild for lazy evaluation."""
        self.cache_valid = False
        if self.enable_range_queries:
            self.sorted_valid = False
    
    def _rebuild_heap_if_needed(self) -> None:
        """Rebuild heap only when necessary (lazy evaluation)."""
        if not self.cache_valid:
            self.heap = [(time, horse_id) for horse_id, time in self.horse_times.items()]
            heapq.heapify(self.heap)
            self.cache_valid = True
    
    def _rebuild_sorted_if_needed(self) -> None:
        """Rebuild sorted list only when necessary."""
        if self.enable_range_queries and not self.sorted_valid:
            self.sorted_times = sorted(self.horse_times.items(), key=lambda x: x[1])
            self.sorted_valid = True
    
    def get_top_performers(self, n: int = 5) -> List[Tuple[str, float]]:
        """Get top n performers with caching optimization."""
        with self.lock:
            self.query_count += 1
            
            # Check cache for common queries
            if (n <= self.cache_top_k and 
                self.cached_top_results is not None and 
                len(self.cached_top_results) >= n):
                self.cache_hits += 1
                return self.cached_top_results[:n]
            
            # Cache miss - compute and cache
            self.cache_misses += 1
            self._rebuild_heap_if_needed()
            
            result = heapq.nsmallest(n, self.heap)
            # Convert from (time, horse_id) to (horse_id, time)
            result = [(horse_id, time) for time, horse_id in result]
            
            # Cache the result if it's within our cache size
            if n <= self.cache_top_k:
                heap_result = heapq.nsmallest(self.cache_top_k, self.heap)
                self.cached_top_results = [(horse_id, time) for time, horse_id in heap_result]
            
            return result
    
    def get_top_performers_in_time_range(self, min_time: float, max_time: float, 
                                       limit: int = 10) -> List[Tuple[float, str]]:
        """Get top performers within a specific time range."""
        if not self.enable_range_queries:
            # Fallback to linear search
            results = [(time, horse_id) for horse_id, time in self.horse_times.items()
                      if min_time <= time <= max_time]
            return sorted(results)[:limit]
        
        with self.lock:
            self._rebuild_sorted_if_needed()
            
            # Linear search through sorted list since it's sorted by time
            range_results = []
            for horse_id, time in self.sorted_times:
                if min_time <= time <= max_time:
                    range_results.append((time, horse_id))
                elif time > max_time:
                    break  # Since sorted by time, no need to continue
            
            return range_results[:limit]
    
    def get_horse_rank(self, horse_id: str) -> int:
        """Get rank with optimized search."""
        if horse_id not in self.entries:
            return -1
        
        with self.lock:
            target_time = self.horse_times[horse_id]
            
            # Count horses with better times
            better_count = sum(1 for time in self.horse_times.values() 
                             if time < target_time)
            
            return better_count + 1
    
    def get_horse_rank_optimized(self, horse_id: str) -> int:
        """Optimized rank calculation using sorted list."""
        if horse_id not in self.entries:
            return -1
        
        if not self.enable_range_queries:
            return self.get_horse_rank(horse_id)
        
        with self.lock:
            self._rebuild_sorted_if_needed()
            target_time = self.horse_times[horse_id]
            
            # Count horses with better (lower) times
            better_count = sum(1 for h_id, time in self.sorted_times 
                             if time < target_time)
            
            return better_count + 1
    
    def get_percentile_stats(self) -> Dict[str, float]:
        """Get performance percentile statistics."""
        if not self.enable_range_queries:
            times = sorted(self.horse_times.values())
        else:
            with self.lock:
                self._rebuild_sorted_if_needed()
                times = [time for horse_id, time in self.sorted_times]
        
        if not times:
            return {}
        
        n = len(times)
        return {
            'min': times[0],
            'max': times[-1],
            'median': times[n // 2],
            'p25': times[n // 4],
            'p75': times[3 * n // 4],
            'p90': times[int(0.9 * n)],
            'p95': times[int(0.95 * n)],
            'mean': sum(times) / n
        }
    
    def update_horse_time(self, horse_id: str, new_time: float) -> bool:
        """Update a horse's time with optimization."""
        with self.lock:
            if horse_id not in self.entries:
                return False
            
            old_time = self.horse_times[horse_id]
            if new_time < old_time:
                self.horse_times[horse_id] = new_time
                self._invalidate_caches()
                return True
            
            return False
    
    def remove_horse(self, horse_id: str) -> bool:
        """Remove a horse from the leaderboard."""
        with self.lock:
            if horse_id not in self.entries:
                return False
            
            self.entries.remove(horse_id)
            del self.horse_times[horse_id]
            self._invalidate_caches()
            return True
    
    def _invalidate_caches(self) -> None:
        """Invalidate all cached data."""
        self.cached_top_results = None
        self.cache_valid = False
        if self.enable_range_queries:
            self.sorted_valid = False
    
    def get_performance_stats(self) -> Dict[str, any]:
        """Get performance statistics."""
        total_queries = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total_queries * 100) if total_queries > 0 else 0
        
        return {
            'total_horses': len(self.entries),
            'update_count': self.update_count,
            'query_count': self.query_count,
            'cache_hit_rate': hit_rate,
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'heap_size': len(self.heap),
            'cached_results_size': len(self.cached_top_results) if self.cached_top_results else 0
        }
    
    def compact(self) -> None:
        """Compact internal data structures for memory efficiency."""
        with self.lock:
            # Rebuild heap to remove stale entries
            self._rebuild_heap_if_needed()
            
            # Rebuild sorted list if enabled
            if self.enable_range_queries:
                self._rebuild_sorted_if_needed()
            
            # Clear cache to free memory
            self.cached_top_results = None
    
    def get_memory_usage_estimate(self) -> Dict[str, int]:
        """Estimate memory usage of different components."""
        import sys
        
        heap_size = sys.getsizeof(self.heap)
        for item in self.heap:
            heap_size += sys.getsizeof(item)
        
        entries_size = sys.getsizeof(self.entries)
        times_size = sys.getsizeof(self.horse_times)
        
        cache_size = 0
        if self.cached_top_results:
            cache_size = sys.getsizeof(self.cached_top_results)
        
        sorted_size = 0
        if self.enable_range_queries:
            sorted_size = sys.getsizeof(self.sorted_times)
        
        return {
            'heap': heap_size,
            'entries_set': entries_size,
            'horse_times': times_size,
            'cache': cache_size,
            'sorted_list': sorted_size,
            'total': heap_size + entries_size + times_size + cache_size + sorted_size
        }
    
    def size(self) -> int:
        """Get the number of horses in the leaderboard."""
        return len(self.entries)
    
    def get_all_results(self) -> List[Tuple[float, str]]:
        """Get all results sorted by performance."""
        with self.lock:
            if self.enable_range_queries:
                self._rebuild_sorted_if_needed()
                return [(time, horse_id) for horse_id, time in self.sorted_times]
            else:
                return sorted([(time, horse_id) for horse_id, time in self.horse_times.items()])
