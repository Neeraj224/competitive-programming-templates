import math

class SparseTable:
    def __init__(self, nums):
        # Sparse Table is used for static range queries
        #
        # Key idea:
        # precompute answers for intervals of size 2^k
        #
        # st[k][i] => answer for range starting at i of length 2^k
        #
        # For RMQ (min), we can answer any query using two overlapping blocks

        self.n = len(nums)
        self.LOG = int(math.log2(self.n)) + 1

        self.st = [[0] * self.n for _ in range(self.LOG)]

        # base layer => intervals of size 1
        for i in range(self.n):
            self.st[0][i] = nums[i]

        # build larger intervals using previously computed values
        for k in range(1, self.LOG):
            for i in range(self.n - (1 << k) + 1):
                self.st[k][i] = min(
                    self.st[k - 1][i],
                    self.st[k - 1][i + (1 << (k - 1))]
                )

    def query(self, l, r):
        # length of query interval
        length = r - l + 1

        # find largest power of 2 within range
        k = int(math.log2(length))

        # combine two overlapping intervals
        return min(
            self.st[k][l],
            self.st[k][r - (1 << k) + 1]
        )


def main():
    nums = [1, 3, 2, 7, 9, 11]
    st = SparseTable(nums)

    print(st.query(1, 4))  # 2


if __name__ == "__main__":
    main()