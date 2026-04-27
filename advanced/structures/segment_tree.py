class SegmentTree:
    def __init__(self, nums):
        # Segment Tree represents an array as a binary tree of ranges
        #
        # each node stores aggregate over a segment (sum here)
        # root => entire range
        # children => left and right halves
        #
        # allows:
        # - range queries in O(log n)
        # - point updates in O(log n)

        self.n = len(nums)
        self.tree = [0] * (4 * self.n)

        self.build(0, 0, self.n - 1, nums)

    def build(self, idx, left, right, nums):
        # build tree recursively
        #
        # leaf node represents a single element
        # internal node combines results of children

        if left == right:
            self.tree[idx] = nums[left]
            return

        mid = (left + right) // 2

        self.build(2 * idx + 1, left, mid, nums)
        self.build(2 * idx + 2, mid + 1, right, nums)

        # merge step defines what the tree represents
        # here it's sum, could be min/max/gcd etc
        self.tree[idx] = self.tree[2 * idx + 1] + self.tree[2 * idx + 2]

    def update(self, pos, val):
        # update a single element
        #
        # traverse down to leaf and update
        # then recompute affected segments on the way back

        self._update(0, 0, self.n - 1, pos, val)

    def _update(self, idx, left, right, pos, val):
        # reached target leaf

        if left == right:
            self.tree[idx] = val
            return

        mid = (left + right) // 2

        # go to the segment that contains pos
        if pos <= mid:
            self._update(2 * idx + 1, left, mid, pos, val)
        else:
            self._update(2 * idx + 2, mid + 1, right, pos, val)

        # recompute current node after child update
        self.tree[idx] = self.tree[2 * idx + 1] + self.tree[2 * idx + 2]

    def query(self, l, r):
        # query range [l, r]

        return self._query(0, 0, self.n - 1, l, r)

    def _query(self, idx, left, right, l, r):
        # three cases:
        # no overlap => ignore
        # full overlap => use stored value
        # partial overlap => split

        if r < left or l > right:
            return 0

        if l <= left and right <= r:
            return self.tree[idx]

        mid = (left + right) // 2

        return (
            self._query(2 * idx + 1, left, mid, l, r) +
            self._query(2 * idx + 2, mid + 1, right, l, r)
        )


def main():
    nums = [1, 3, 5, 7, 9]
    st = SegmentTree(nums)

    print(st.query(1, 3))  # 15

    st.update(2, 10)

    print(st.query(1, 3))  # 20


if __name__ == "__main__":
    main()