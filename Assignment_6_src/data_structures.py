"""
This module implements fundamental data structures with minimal complexity.
"""


class SimpleStack:
    """Simple stack using Python list."""
    
    def __init__(self):
        self.items = []
    
    def push(self, item):
        """Add item to top."""
        self.items.append(item)
    
    def pop(self):
        """Remove and return top item."""
        if not self.items:
            raise IndexError("Stack is empty")
        return self.items.pop()
    
    def peek(self):
        """Return top item without removing."""
        if not self.items:
            raise IndexError("Stack is empty")
        return self.items[-1]
    
    def is_empty(self):
        """Check if stack is empty."""
        return len(self.items) == 0
    
    def size(self):
        """Return number of items."""
        return len(self.items)


class SimpleQueue:
    """Simple queue using Python list."""
    
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        """Add item to rear."""
        self.items.append(item)
    
    def dequeue(self):
        """Remove and return front item."""
        if not self.items:
            raise IndexError("Queue is empty")
        return self.items.pop(0)  # O(n) but simple
    
    def peek(self):
        """Return front item without removing."""
        if not self.items:
            raise IndexError("Queue is empty")
        return self.items[0]
    
    def is_empty(self):
        """Check if queue is empty."""
        return len(self.items) == 0
    
    def size(self):
        """Return number of items."""
        return len(self.items)


class ListNode:
    """Simple node for linked list."""
    
    def __init__(self, data):
        self.data = data
        self.next = None


class SimpleLinkedList:
    """Simple singly linked list."""
    
    def __init__(self):
        self.head = None
        self.size = 0
    
    def insert_front(self, data):
        """Insert at beginning. O(1)"""
        new_node = ListNode(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
    
    def insert_back(self, data):
        """Insert at end. O(n)"""
        new_node = ListNode(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1
    
    def delete_front(self):
        """Delete from beginning. O(1)"""
        if not self.head:
            raise IndexError("List is empty")
        data = self.head.data
        self.head = self.head.next
        self.size -= 1
        return data
    
    def search(self, data):
        """Search for data. O(n)"""
        current = self.head
        index = 0
        while current:
            if current.data == data:
                return index
            current = current.next
            index += 1
        return -1
    
    def to_list(self):
        """Convert to Python list for easy viewing."""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
    
    def __len__(self):
        return self.size


class TreeNode:
    """Simple tree node."""
    
    def __init__(self, data):
        self.data = data
        self.children = []


class SimpleTree:
    """Simple rooted tree."""
    
    def __init__(self, root_data):
        self.root = TreeNode(root_data)
        self.size = 1
    
    def add_child(self, parent_data, child_data):
        """Add child to parent node."""
        parent = self._find_node(self.root, parent_data)
        if parent:
            parent.children.append(TreeNode(child_data))
            self.size += 1
            return True
        return False
    
    def _find_node(self, node, data):
        """Find node with given data."""
        if node.data == data:
            return node
        for child in node.children:
            result = self._find_node(child, data)
            if result:
                return result
        return None
    
    def preorder(self):
        """Preorder traversal."""
        result = []
        self._preorder_helper(self.root, result)
        return result
    
    def _preorder_helper(self, node, result):
        """Helper for preorder traversal."""
        result.append(node.data)
        for child in node.children:
            self._preorder_helper(child, result)
    
    def __len__(self):
        return self.size


# Demo function
def demo():
    """Demonstrate all data structures."""
    print("Data Structures Demo")
    print("=" * 25)
    
    # Stack demo
    print("\nStack:")
    stack = SimpleStack()
    for i in [1, 2, 3]:
        stack.push(i)
        print(f"Push {i}, size: {stack.size()}")
    print(f"Pop: {stack.pop()}, size: {stack.size()}")
    
    # Queue demo
    print("\nQueue:")
    queue = SimpleQueue()
    for i in [1, 2, 3]:
        queue.enqueue(i)
        print(f"Enqueue {i}, size: {queue.size()}")
    print(f"Dequeue: {queue.dequeue()}, size: {queue.size()}")
    
    # Linked List demo
    print("\nLinked List:")
    ll = SimpleLinkedList()
    ll.insert_front(1)
    ll.insert_back(2)
    ll.insert_back(3)
    print(f"List: {ll.to_list()}")
    print(f"Search 2: index {ll.search(2)}")
    print(f"Delete front: {ll.delete_front()}")
    print(f"List: {ll.to_list()}")
    
    # Tree demo
    print("\nTree:")
    tree = SimpleTree("root")
    tree.add_child("root", "A")
    tree.add_child("root", "B")
    tree.add_child("A", "C")
    print(f"Preorder: {tree.preorder()}")
    print(f"Size: {len(tree)}")


if __name__ == "__main__":
    demo()
