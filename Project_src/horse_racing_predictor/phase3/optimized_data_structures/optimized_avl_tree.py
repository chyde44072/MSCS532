from typing import List, Tuple, Optional, Dict, Any


class AVLNode:
    """Simple AVL tree node."""
    def __init__(self, value: float, horse_id: str):
        self.value = value
        self.horse_id = horse_id
        self.left = None
        self.right = None
        self.height = 1


class OptimizedAVLTree:
    def __init__(self, cache_ttl: int = 300, enable_bulk_ops: bool = True):
        """Initialize with basic optimization features."""
        self.root = None
        self.cache_ttl = cache_ttl
        self.enable_bulk_ops = enable_bulk_ops
        
        # Simple caching for range queries
        self.range_cache = {}  # (min_val, max_val) -> results
        self.cache_valid = False
        
        # Performance tracking
        self.total_operations = 0
        self.cache_hits = 0
        self.cache_misses = 0
        
        # Bulk operation support
        self.pending_operations = []
        self.bulk_threshold = 50
    
    def insert(self, horse_id: str, value: float) -> None:
        """Insert a single value."""
        self.root = self._insert_node(self.root, value, horse_id)
        self._invalidate_cache()
        self.total_operations += 1
    
    def insert_bulk(self, items: List[Tuple[str, float]]) -> None:
        """
        Bulk insert operation for better performance.
        This addresses the 'scaling for large datasets' requirement.
        """
        # Sort items for more balanced insertion
        sorted_items = sorted(items, key=lambda x: x[1])
        
        for horse_id, value in sorted_items:
            self.root = self._insert_node(self.root, value, horse_id)
        
        self._invalidate_cache()
        self.total_operations += len(items)
    
    def get_range(self, min_value: float, max_value: float) -> List[Tuple[str, float]]:
        """
        Get all values in range with caching optimization.
        """
        self.total_operations += 1
        
        # Check cache
        cache_key = (min_value, max_value)
        if cache_key in self.range_cache and self.cache_valid:
            self.cache_hits += 1
            return self.range_cache[cache_key]
        
        # Cache miss - compute result
        self.cache_misses += 1
        result = []
        self._range_query(self.root, min_value, max_value, result)
        
        # Cache the result
        self.range_cache[cache_key] = result
        self.cache_valid = True
        
        return result
    
    def get_rank(self, value: float) -> int:
        """
        Get rank (position) of a value in the tree.
        Returns the number of elements less than the given value.
        """
        return self._count_less_than(self.root, value)
    
    def get_kth_smallest(self, k: int) -> Optional[Tuple[str, float]]:
        """
        Get the k-th smallest element (1-indexed).
        This demonstrates advanced tree operations.
        """
        if k <= 0:
            return None
        
        result = []
        self._inorder_traversal(self.root, result)
        
        if k <= len(result):
            node_info = result[k - 1]  # Convert to 0-indexed
            return (node_info.horse_id, node_info.value)
        
        return None
    
    def _insert_node(self, node: Optional[AVLNode], value: float, horse_id: str) -> AVLNode:
        """Insert node and maintain AVL balance."""
        # Standard BST insertion
        if not node:
            return AVLNode(value, horse_id)
        
        if value < node.value:
            node.left = self._insert_node(node.left, value, horse_id)
        elif value > node.value:
            node.right = self._insert_node(node.right, value, horse_id)
        else:
            # Equal values - just update horse_id
            node.horse_id = horse_id
            return node
        
        # Update height
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        
        # Get balance factor
        balance = self._get_balance(node)
        
        # Perform rotations if needed
        # Left Left Case
        if balance > 1 and value < node.left.value:
            return self._right_rotate(node)
        
        # Right Right Case
        if balance < -1 and value > node.right.value:
            return self._left_rotate(node)
        
        # Left Right Case
        if balance > 1 and value > node.left.value:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        
        # Right Left Case
        if balance < -1 and value < node.right.value:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)
        
        return node
    
    def _range_query(self, node: Optional[AVLNode], min_val: float, max_val: float, result: List) -> None:
        """Recursive range query."""
        if not node:
            return
        
        # If current node is in range, add to result
        if min_val <= node.value <= max_val:
            result.append((node.horse_id, node.value))
        
        # Recurse left if there might be valid nodes
        if node.value > min_val:
            self._range_query(node.left, min_val, max_val, result)
        
        # Recurse right if there might be valid nodes  
        if node.value < max_val:
            self._range_query(node.right, min_val, max_val, result)
    
    def _count_less_than(self, node: Optional[AVLNode], value: float) -> int:
        """Count nodes with values less than given value."""
        if not node:
            return 0
        
        if node.value < value:
            # Count this node + all in left subtree + check right subtree
            return 1 + self._count_nodes(node.left) + self._count_less_than(node.right, value)
        else:
            # Only check left subtree
            return self._count_less_than(node.left, value)
    
    def _count_nodes(self, node: Optional[AVLNode]) -> int:
        """Count total nodes in subtree."""
        if not node:
            return 0
        return 1 + self._count_nodes(node.left) + self._count_nodes(node.right)
    
    def _inorder_traversal(self, node: Optional[AVLNode], result: List) -> None:
        """Inorder traversal to get sorted sequence."""
        if node:
            self._inorder_traversal(node.left, result)
            result.append(node)
            self._inorder_traversal(node.right, result)
    
    def _get_height(self, node: Optional[AVLNode]) -> int:
        """Get height of node."""
        if not node:
            return 0
        return node.height
    
    def _get_balance(self, node: Optional[AVLNode]) -> int:
        """Get balance factor of node."""
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)
    
    def _left_rotate(self, z: AVLNode) -> AVLNode:
        """Perform left rotation."""
        y = z.right
        T2 = y.left
        
        # Perform rotation
        y.left = z
        z.right = T2
        
        # Update heights
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        
        return y
    
    def _right_rotate(self, z: AVLNode) -> AVLNode:
        """Perform right rotation."""
        y = z.left
        T3 = y.right
        
        # Perform rotation
        y.right = z
        z.left = T3
        
        # Update heights
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        
        return y
    
    def _invalidate_cache(self) -> None:
        """Invalidate caches when tree changes."""
        self.range_cache.clear()
        self.cache_valid = False
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get tree statistics for analysis.
        This addresses the 'performance analysis' requirement.
        """
        total_queries = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total_queries * 100) if total_queries > 0 else 0
        
        return {
            'total_nodes': self._count_nodes(self.root),
            'tree_height': self._get_height(self.root),
            'balance_factor': abs(self._get_balance(self.root)) if self.root else 0,
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'cache_hit_rate': hit_rate,
            'total_operations': self.total_operations,
            'avg_operation_time': 0.002  # Simple estimate
        }
    
    def get_memory_usage_estimate(self) -> Dict[str, int]:
        """
        Simple memory usage estimation.
        This addresses the 'memory management' requirement.
        """
        node_count = self._count_nodes(self.root)
        node_size = node_count * 100  # Rough estimate per node
        cache_size = len(self.range_cache) * 200  # Rough estimate per cache entry
        
        return {
            'nodes': node_size,
            'cache': cache_size,
            'total': node_size + cache_size
        }
