"""
hash_table.py

Implements a simple hash table for storing and managing horse metadata.
"""

from typing import Dict, Any, Optional, List

class HorseDatabase:
    """
    Hash table for storing and managing horse metadata.
    Keys are horse IDs, values are dictionaries of horse data.
    """
    def __init__(self):
        # Initialize the internal dictionary to store horse data
        self.db: Dict[str, Dict[str, Any]] = {}

    def add_horse(self, horse_id: str, data: Dict[str, Any]) -> None:
        # Adds a horse's profile to the database
        self.db[horse_id] = data

    def get_horse(self, horse_id: str) -> Optional[Dict[str, Any]]:
        # Retrieves a horse's data using its unique ID
        return self.db.get(horse_id, None)

    def update_performance(self, horse_id: str, new_data: Dict[str, Any]) -> None:
        # Updates specific performance data for a horse
        if horse_id in self.db:
            self.db[horse_id].update(new_data)

    def remove_horse(self, horse_id: str) -> None:
        # Deletes a horse record from the database
        self.db.pop(horse_id, None)

    def list_horses(self) -> List[str]:
        # Returns a list of all horse IDs in the database
        return list(self.db.keys())

    def __len__(self) -> int:
        # Returns the number of horses in the database
        return len(self.db)