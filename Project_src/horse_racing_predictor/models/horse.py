from dataclasses import dataclass
from typing import List

@dataclass
class Horse:
    horse_id: str
    name: str
    avg_speed: float
    win_ratio: float
    preferred_conditions: List[str]