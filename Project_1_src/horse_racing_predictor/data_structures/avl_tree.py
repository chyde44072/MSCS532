# AVL Tree for sorted metrics (e.g., speed, win ratio)

from typing import Optional, List, Tuple

class AVLNode:
    def __init__(self, horse_id: str, metric: float):
        self.id = horse_id  # Horse identifier
        self.metric = metric  # Metric value (e.g., speed)
        self.left: Optional['AVLNode'] = None
        self.right: Optional['AVLNode'] = None
        self.height: int = 1

class AVLTree:
    """
    AVL Tree for storing horses sorted by a specific metric.
    """
    def insert(self, root: Optional[AVLNode], horse_id: str, metric: float) -> AVLNode:
        # Insert a new node and keep the tree balanced
        if not root:
            return AVLNode(horse_id, metric)
        elif metric < root.metric:
            root.left = self.insert(root.left, horse_id, metric)
        else:
            root.right = self.insert(root.right, horse_id, metric)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # Balance the tree
        if balance > 1 and metric < root.left.metric:
            return self.right_rotate(root)
        if balance < -1 and metric >= root.right.metric:
            return self.left_rotate(root)
        if balance > 1 and metric >= root.left.metric:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and metric < root.right.metric:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def in_order(self, root: Optional[AVLNode]) -> List[Tuple[str, float]]:
        # In-order traversal of the tree
        if not root:
            return []
        return self.in_order(root.left) + [(root.id, root.metric)] + self.in_order(root.right)

    def get_top_n(self, root: Optional[AVLNode], n: int = 5) -> List[Tuple[str, float]]:
        # Get top n horses by metric
        all_nodes = self.in_order(root)
        return sorted(all_nodes, key=lambda x: x[1], reverse=True)[:n]

    def get_height(self, node: Optional[AVLNode]) -> int:
        # Get the height of a node
        return node.height if node else 0

    def get_balance(self, node: Optional[AVLNode]) -> int:
        # Get the balance factor of a node
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def left_rotate(self, z: AVLNode) -> AVLNode:
        # Perform a left rotation
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, y: AVLNode) -> AVLNode:
        # Perform a right rotation
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        return x