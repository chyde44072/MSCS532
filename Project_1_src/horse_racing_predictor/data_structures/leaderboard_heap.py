# Min-heap for live leaderboard rankings
import heapq
from typing import List, Tuple

class Leaderboard:
    """
    Min-heap leaderboard for tracking top-performing horses by race time.
    """
    def __init__(self):
        # Initialize the heap and a set to track horse entries
        self.heap: List[Tuple[float, str]] = []  # [(time, horse_id)]
        self.entries: set[str] = set()

    def add_result(self, horse_id: str, time: float) -> None:
        # Add a horse's race result to the leaderboard if not already present
        if horse_id not in self.entries:
            heapq.heappush(self.heap, (time, horse_id))
            self.entries.add(horse_id)

    def get_top_performers(self, n: int = 5) -> List[Tuple[float, str]]:
        # Get the top n performers (lowest times)
        return heapq.nsmallest(n, self.heap)