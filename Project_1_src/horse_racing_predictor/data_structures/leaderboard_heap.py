import heapq
from typing import List, Tuple, Dict

class Leaderboard:
    """
    Min-heap leaderboard for tracking top-performing horses by race time.
    Enhanced with update capability and multiple performance metrics.
    """
    def __init__(self):
        # Initialize the heap and tracking dictionaries
        self.heap: List[Tuple[float, str]] = []  # [(time, horse_id)]
        self.entries: set[str] = set()
        self.horse_times: Dict[str, float] = {}  # Track current best time per horse

    def add_result(self, horse_id: str, time: float) -> None:
        """Add a horse's race result to the leaderboard."""
        if horse_id not in self.entries:
            heapq.heappush(self.heap, (time, horse_id))
            self.entries.add(horse_id)
            self.horse_times[horse_id] = time
        else:
            # Update if this is a better (lower) time
            if time < self.horse_times[horse_id]:
                self.horse_times[horse_id] = time
                # Rebuild heap to maintain correct ordering
                self._rebuild_heap()

    def _rebuild_heap(self) -> None:
        """Rebuild heap with current best times."""
        self.heap = [(time, horse_id) for horse_id, time in self.horse_times.items()]
        heapq.heapify(self.heap)

    def get_top_performers(self, n: int = 5) -> List[Tuple[float, str]]:
        """Get the top n performers (lowest times)."""
        return heapq.nsmallest(n, self.heap)

    def get_horse_rank(self, horse_id: str) -> int:
        """Get the rank of a specific horse (1-indexed)."""
        if horse_id not in self.entries:
            return -1
        
        sorted_times = sorted(self.heap)
        for i, (time, h_id) in enumerate(sorted_times):
            if h_id == horse_id:
                return i + 1
        return -1

    def remove_horse(self, horse_id: str) -> bool:
        """Remove a horse from the leaderboard."""
        if horse_id in self.entries:
            self.entries.remove(horse_id)
            del self.horse_times[horse_id]
            self._rebuild_heap()
            return True
        return False

    def get_all_results(self) -> List[Tuple[float, str]]:
        """Get all results sorted by performance."""
        return sorted(self.heap)

    def size(self) -> int:
        """Get the number of horses in the leaderboard."""
        return len(self.entries)