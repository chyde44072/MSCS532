from typing import List, Tuple, Optional

class AVLNode:
    """Node class for AVL tree storing horse ranking data."""
    def __init__(self, horse_id: str, win_ratio: float):
        self.horse_id = horse_id
        self.win_ratio = win_ratio
        self.left: Optional['AVLNode'] = None
        self.right: Optional['AVLNode'] = None
        self.height = 1

class AVLTree:
    """
    Self-balancing binary search tree for ranking horses by win ratio.
    Supports efficient range queries and sorted retrieval with O(log n) operations.
    """
    def __init__(self):
        self.root: Optional[AVLNode] = None

    def _get_height(self, node: Optional[AVLNode]) -> int:
        """Get the height of a node."""
        return node.height if node else 0

    def _get_balance(self, node: Optional[AVLNode]) -> int:
        """Get the balance factor of a node."""
        return self._get_height(node.left) - self._get_height(node.right) if node else 0

    def _rotate_right(self, y: AVLNode) -> AVLNode:
        """Perform right rotation."""
        x = y.left
        t2 = x.right

        # Perform rotation
        x.right = y
        y.left = t2

        # Update heights
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))

        return x

    def _rotate_left(self, x: AVLNode) -> AVLNode:
        """Perform left rotation."""
        y = x.right
        t2 = y.left

        # Perform rotation
        y.left = x
        x.right = t2

        # Update heights
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _balance(self, node: AVLNode) -> AVLNode:
        """Balance the node if necessary."""
        balance = self._get_balance(node)

        # Left heavy
        if balance > 1:
            if self._get_balance(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right heavy
        if balance < -1:
            if self._get_balance(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def insert(self, horse_id: str, win_ratio: float) -> None:
        """Insert or update a horse's win ratio."""
        self.root = self._insert(self.root, horse_id, win_ratio)

    def _insert(self, node: Optional[AVLNode], horse_id: str, win_ratio: float) -> AVLNode:
        """Recursive insert with balancing."""
        # Standard BST insertion
        if not node:
            return AVLNode(horse_id, win_ratio)

        if win_ratio < node.win_ratio:
            node.left = self._insert(node.left, horse_id, win_ratio)
        elif win_ratio > node.win_ratio:
            node.right = self._insert(node.right, horse_id, win_ratio)
        else:
            # Update existing horse
            node.horse_id = horse_id
            return node

        # Update height
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        # Balance the node
        return self._balance(node)

    def get_range(self, min_ratio: float, max_ratio: float) -> List[Tuple[str, float]]:
        """Get all horses within a win ratio range."""
        result = []
        self._range_search(self.root, min_ratio, max_ratio, result)
        return result

    def _range_search(self, node: Optional[AVLNode], min_ratio: float, max_ratio: float, result: List[Tuple[str, float]]) -> None:
        """Recursive range search."""
        if not node:
            return

        if min_ratio <= node.win_ratio <= max_ratio:
            result.append((node.horse_id, node.win_ratio))

        if min_ratio < node.win_ratio:
            self._range_search(node.left, min_ratio, max_ratio, result)
        if max_ratio > node.win_ratio:
            self._range_search(node.right, min_ratio, max_ratio, result)

    def get_sorted_list(self) -> List[Tuple[str, float]]:
        """Get all horses sorted by win ratio (ascending)."""
        result = []
        self._inorder_traversal(self.root, result)
        return result

    def _inorder_traversal(self, node: Optional[AVLNode], result: List[Tuple[str, float]]) -> None:
        """Recursive inorder traversal."""
        if node:
            self._inorder_traversal(node.left, result)
            result.append((node.horse_id, node.win_ratio))
            self._inorder_traversal(node.right, result)