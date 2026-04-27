class FenwickTree:
    def __init__(self, n):
        # Fenwick Tree is a compressed representation of prefix sums.
        #
        # Instead of storing all prefix sums explicitly,
        # each index stores sum over a specific range.
        #
        # The range size is determined by the lowest set bit of the index.
        #
        # Example:
        # index 8 (1000) => covers 8 elements
        # index 6 (0110) => covers 2 elements
        #
        # This allows us to jump across ranges efficiently using bit operations.
        #
        # We use 1-based indexing so that i & -i gives the size of range.

        self.n = n
        self.tree = [0] * (n + 1)

    def update(self, i, delta):
        # Goal: add delta to index i
        #
        # Key idea:
        # multiple nodes are responsible for index i,
        # so we must update all of them.
        #
        # We move upward in the structure by adding i & -i,
        # which jumps to the next segment that includes i.

        i += 1

        while i <= self.n:
            self.tree[i] += delta
            i += i & -i

    def query(self, i):
        # Goal: compute prefix sum from 0 to i
        #
        # Key idea:
        # combine contributions from segments that cover [0...i]
        #
        # We move upward toward the root by subtracting i & -i,
        # which removes the last segment and moves to parent.

        i += 1
        res = 0

        while i > 0:
            res += self.tree[i]
            i -= i & -i

        return res

    def range_query(self, l, r):
        # Range sum is derived from prefix sums

        return self.query(r) - self.query(l - 1)


def main():
    ft = FenwickTree(5)

    ft.update(0, 1)
    ft.update(1, 2)
    ft.update(2, 3)

    print(ft.range_query(0, 2))


if __name__ == "__main__":
    main()