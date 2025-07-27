from data_structures.hash_table import HorseDatabase
from data_structures.avl_tree import AVLTree, AVLNode
from data_structures.leaderboard_heap import Leaderboard
from data_structures.data_loader import load_horses_from_excel

if __name__ == "__main__":
    # Initialize Horse Database (Hash Table)
    db = HorseDatabase()
    load_horses_from_excel(r"C:\Users\corey\Documents\Cumberlands\MSCS532\Git\MSCS532_Assignment1\Project_1_src\horse_racing_predictor\horses.xlsx", db)  # Load all horses from Excel

    # Build AVL Tree for win ratio rankings
    tree = AVLTree()
    root = None
    for horse_id, data in db.db.items():
        root = tree.insert(root, horse_id, data["win_ratio"])

    # Create Leaderboard Heap for average speeds
    speed_lb = Leaderboard()
    for horse_id, data in db.db.items():
        if "avg_speed" in data:
            speed_lb.add_result(horse_id, data["avg_speed"])

    # Create Leaderboard Heap for win ratios
    win_lb = Leaderboard()
    for horse_id, data in db.db.items():
        if "win_ratio" in data:
            win_lb.add_result(horse_id, data["win_ratio"])

    # Outputs
    print("Horse Lookup (H001):", db.get_horse("H001"))
    print("Top 2 Win Ratios (AVL Tree):", tree.get_top_n(root, 2))
    print("Leaderboard (Top Speeds):", speed_lb.get_top_performers())
    print("Leaderboard (Top Win Ratios):", win_lb.get_top_performers())