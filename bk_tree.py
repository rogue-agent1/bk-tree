#!/usr/bin/env python3
"""bk_tree - BK-tree for fuzzy string matching using Levenshtein distance."""
import sys

def levenshtein(a, b):
    if len(a) < len(b): a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        curr = [i]
        for j, cb in enumerate(b, 1):
            curr.append(min(prev[j] + 1, curr[j-1] + 1, prev[j-1] + (0 if ca == cb else 1)))
        prev = curr
    return prev[-1]

class BKTree:
    def __init__(self):
        self.root = None
    def add(self, word):
        if self.root is None:
            self.root = (word, {})
            return
        node = self.root
        while True:
            d = levenshtein(word, node[0])
            if d == 0: return
            if d in node[1]:
                node = node[1][d]
            else:
                node[1][d] = (word, {})
                return
    def query(self, word, max_dist):
        if self.root is None: return []
        results = []
        stack = [self.root]
        while stack:
            node = stack.pop()
            d = levenshtein(word, node[0])
            if d <= max_dist:
                results.append((node[0], d))
            for dist, child in node[1].items():
                if d - max_dist <= dist <= d + max_dist:
                    stack.append(child)
        return sorted(results, key=lambda x: x[1])

def test():
    tree = BKTree()
    words = ["book", "back", "cook", "brook", "look", "hook", "books", "cake"]
    for w in words: tree.add(w)
    r = tree.query("book", 1)
    matches = [w for w, d in r]
    assert "book" in matches
    assert "books" in matches
    assert "cook" in matches
    assert "look" in matches
    assert "cake" not in matches
    r2 = tree.query("book", 0)
    assert len(r2) == 1 and r2[0][0] == "book"
    r3 = tree.query("brok", 2)
    assert "brook" in [w for w, d in r3]
    print("bk_tree: all tests passed")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("Usage: bk_tree.py --test")
