import random

class HashTableChaining:
    def __init__(self, size=101):
        self.size = size
        self.table = [[] for _ in range(size)]
        # Universal hash function parameters
        self.p = 10**9 + 7  # Large prime
        self.a = random.randint(1, self.p - 1)
        self.b = random.randint(0, self.p - 1)

    def _hash(self, key):
        # Universal hash function for integers
        return ((self.a * hash(key) + self.b) % self.p) % self.size

    def insert(self, key, value):
        idx = self._hash(key)
        for i, (k, v) in enumerate(self.table[idx]):
            if k == key:
                self.table[idx][i] = (key, value)  # Update existing
                return
        self.table[idx].append((key, value))

    def search(self, key):
        idx = self._hash(key)
        for k, v in self.table[idx]:
            if k == key:
                return v
        return None

    def delete(self, key):
        idx = self._hash(key)
        for i, (k, v) in enumerate(self.table[idx]):
            if k == key:
                del self.table[idx][i]
                return True
        return False

    def __str__(self):
        return str(self.table)