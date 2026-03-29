#!/usr/bin/env python3
"""BK-tree for fuzzy string matching using edit distance."""
import sys

def levenshtein(a, b):
    if len(a) < len(b): a, b = b, a
    prev = list(range(len(b)+1))
    for i, ca in enumerate(a):
        curr = [i+1]
        for j, cb in enumerate(b):
            curr.append(min(prev[j] + (ca != cb), prev[j+1]+1, curr[j]+1))
        prev = curr
    return prev[-1]

class BKTree:
    def __init__(self, dist_fn=levenshtein):
        self.root = None
        self.dist_fn = dist_fn
    def add(self, word):
        if not self.root:
            self.root = (word, {})
            return
        node = self.root
        while True:
            d = self.dist_fn(word, node[0])
            if d == 0: return
            if d in node[1]:
                node = node[1][d]
            else:
                node[1][d] = (word, {})
                return
    def query(self, word, max_dist):
        if not self.root: return []
        results, stack = [], [self.root]
        while stack:
            node = stack.pop()
            d = self.dist_fn(word, node[0])
            if d <= max_dist:
                results.append((node[0], d))
            for dist, child in node[1].items():
                if d - max_dist <= dist <= d + max_dist:
                    stack.append(child)
        return results

def test():
    bk = BKTree()
    words = ["book","back","cook","hook","look","took","books","brook"]
    for w in words:
        bk.add(w)
    r = bk.query("book", 1)
    found = {w for w,d in r}
    assert "book" in found
    assert "hook" in found or "cook" in found or "look" in found or "took" in found or "books" in found
    assert "brook" in found  # dist 1 (delete r)
    r2 = bk.query("book", 0)
    assert len(r2) == 1 and r2[0][0] == "book"
    print("  bk_tree: ALL TESTS PASSED")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("BK-tree fuzzy string matcher")
