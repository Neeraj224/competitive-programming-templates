from math import log2, ceil
from collections import defaultdict


class BinaryLifting:
    def __init__(self, n, edges, root=0):
        # Binary lifting precomputes ancestors at powers of 2
        #
        # up[node][k] => 2^k-th ancestor of node
        #
        # this allows jumping upward in O(log n)
        #
        # also maintain depth of each node for LCA

        self.n = n
        self.LOG = ceil(log2(n)) + 1

        self.graph = defaultdict(list)

        for u, v in edges:
            self.graph[u].append(v)
            self.graph[v].append(u)

        self.up = [[-1] * self.LOG for _ in range(n)]
        self.depth = [0] * n

        self.dfs(root, -1)

        # build binary lifting table
        # each level uses previously computed values
        for k in range(1, self.LOG):
            for node in range(n):
                if self.up[node][k - 1] != -1:
                    self.up[node][k] = self.up[self.up[node][k - 1]][k - 1]


    def dfs(self, node, parent):
        # DFS to initialize:
        # - depth of each node
        # - immediate parent (2^0 ancestor)

        self.up[node][0] = parent

        for nei in self.graph[node]:
            if nei == parent:
                continue

            self.depth[nei] = self.depth[node] + 1
            self.dfs(nei, node)


    def kth_ancestor(self, node, k):
        # move node up by k steps
        #
        # decompose k into powers of 2
        # jump accordingly using precomputed table

        for i in range(self.LOG):
            if k & (1 << i):
                node = self.up[node][i]

                if node == -1:
                    break

        return node


    def lca(self, u, v):
        # bring both nodes to same depth
        # then lift both together until parents match

        if self.depth[u] < self.depth[v]:
            u, v = v, u

        # lift u up to match depth of v
        diff = self.depth[u] - self.depth[v]
        u = self.kth_ancestor(u, diff)

        # if they meet, that's the LCA
        if u == v:
            return u

        # lift both nodes from highest power down
        # stop just before they diverge
        for i in reversed(range(self.LOG)):
            if self.up[u][i] != self.up[v][i]:
                u = self.up[u][i]
                v = self.up[v][i]

        # parent of both is LCA
        return self.up[u][0]


    def distance(self, u, v):
        # distance in tree = depth[u] + depth[v] - 2 * depth[lca]

        lca = self.lca(u, v)
        return self.depth[u] + self.depth[v] - 2 * self.depth[lca]


def main():
    # tree:
    # 0
    # ├── 1
    # │   └── 3
    # └── 2
    #     └── 4

    edges = [
        (0, 1),
        (0, 2),
        (1, 3),
        (2, 4)
    ]

    bl = BinaryLifting(5, edges, 0)

    print(bl.kth_ancestor(3, 1))  # 1
    print(bl.kth_ancestor(3, 2))  # 0

    print(bl.lca(3, 4))  # 0
    print(bl.lca(3, 1))  # 1

    print(bl.distance(3, 4))  # 4


if __name__ == "__main__":
    main()