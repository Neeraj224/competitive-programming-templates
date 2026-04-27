class LazySegmentTree:
    def __init__(self, nums):
        # Segment Tree stores range aggregates (sum here).
        #
        # Problem:
        # range updates are expensive if we update all elements directly.
        #
        # Solution:
        # Lazy propagation.
        #
        # Instead of updating immediately,
        # we store "pending updates" in lazy array.
        #
        # Updates are applied only when required.

        self.n = len(nums)
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)

        self.build(0, 0, self.n - 1, nums)

    def build(self, idx, left, right, nums):
        # Standard segment tree construction

        if left == right:
            self.tree[idx] = nums[left]
            return

        mid = (left + right) // 2

        self.build(2 * idx + 1, left, mid, nums)
        self.build(2 * idx + 2, mid + 1, right, nums)

        self.tree[idx] = self.tree[2 * idx + 1] + self.tree[2 * idx + 2]

    def push(self, idx, left, right):
        # Apply pending update stored at this node
        #
        # If this node has a lazy value,
        # it means this entire segment should be incremented.
        #
        # Instead of pushing updates eagerly,
        # we apply them when visiting the node.

        if self.lazy[idx] != 0:
            self.tree[idx] += (right - left + 1) * self.lazy[idx]

            # propagate to children if not a leaf
            if left != right:
                self.lazy[2 * idx + 1] += self.lazy[idx]
                self.lazy[2 * idx + 2] += self.lazy[idx]

            self.lazy[idx] = 0

    def update_range(self, l, r, val):
        self._update(0, 0, self.n - 1, l, r, val)

    def _update(self, idx, left, right, l, r, val):
        # Always resolve pending updates first
        # ensures correctness before further recursion

        self.push(idx, left, right)

        # no overlap
        if r < left or l > right:
            return

        # full overlap
        # store update lazily instead of going deeper
        if l <= left and right <= r:
            self.lazy[idx] += val
            self.push(idx, left, right)
            return

        # partial overlap => split further
        mid = (left + right) // 2

        self._update(2 * idx + 1, left, mid, l, r, val)
        self._update(2 * idx + 2, mid + 1, right, l, r, val)

        self.tree[idx] = self.tree[2 * idx + 1] + self.tree[2 * idx + 2]

    def query(self, l, r):
        return self._query(0, 0, self.n - 1, l, r)

    def _query(self, idx, left, right, l, r):
        # resolve pending updates before querying

        self.push(idx, left, right)

        # no overlap
        if r < left or l > right:
            return 0

        # full overlap
        if l <= left and right <= r:
            return self.tree[idx]

        # partial overlap
        mid = (left + right) // 2

        return (
            self._query(2 * idx + 1, left, mid, l, r) +
            self._query(2 * idx + 2, mid + 1, right, l, r)
        )


def main():
    nums = [1, 2, 3, 4, 5]
    st = LazySegmentTree(nums)

    print(st.query(0, 4))

    st.update_range(1, 3, 2)

    print(st.query(0, 4))


if __name__ == "__main__":
    main()