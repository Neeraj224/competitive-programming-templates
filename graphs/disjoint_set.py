"""
    NOTE: A Disjoint Set Data Structure is also called a Union Find Data Structure.
    Two sets are called disjoint sets if they don't have any element in common. 
    The disjoint set data structure is used to store such sets. 
    It supports following operations:
        - Merging two disjoint sets to a single set using Union operation.
        - Finding representative of a disjoint set using Find operation.
        - Check if two elements belong to same set or not. We mainly find 
          representative of both and check if same.
"""

# DSU (Disjoint Set Union):
# group elements into disjoint sets (no overlap)

# idea:
# each element belongs to a set, represented by a "root" (leader)
# if two elements have the same root => they are in the same group

# data structure:
# parent[i] stores the parent of i
# if parent[i] == i => i is the root (representative)

# find(x):
# follow parent pointers until reaching root
# returns the representative of x's set

# union(x, y):
# find roots of x and y
# if different => attach one root to the other (merge sets)

class UnionFind:
    def __init__(self, size):
        """
            Example:
            size = 5

            parent = [0, 1, 2, 3, 4]
            size   = [1, 1, 1, 1, 1]
            rank   = [0, 0, 0, 0, 0]

            each node starts as its own set
        """
        # parent[i] stores the parent of node i
        self.parent = list(range(size))

        # size[i] stores size of the set rooted at i
        # meaningful only if i is a root
        self.size = [1] * size

        # rank[i] stores approximate tree height for root i
        # meaningful only if i is a root
        self.rank = [0] * size
    
    def find(self, u):
        """
            find root of u with path compression

            Example:
            3 -> 2 -> 1 -> 0

            after find(3):
            parent[3], parent[2], parent[1] can all directly point to 0
        """
        # if u is not the root, keep moving upward
        # and also compress the path while coming back
        if u != self.parent[u]:
            self.parent[u] = self.find(self.parent[u])

        # return the final root
        return self.parent[u]

    def union_by_size(self, u, v):
        """
            merge sets using size
            smaller set gets attached under bigger set
        """
        # find roots of both nodes
        u_rep = self.find(u)
        v_rep = self.find(v)

        # if both already belong to same set, nothing to merge
        if u_rep == v_rep:
            return

        # if u's set is smaller, attach it under v's root
        if self.size[u_rep] < self.size[v_rep]:
            # make u's root point to v's root
            self.parent[u_rep] = v_rep
            # update size of new combined set at v's root
            self.size[v_rep] += self.size[u_rep]
        else:
            # otherwise attach v's set under u's root
            self.parent[v_rep] = u_rep
            # update size of new combined set at u's root
            self.size[u_rep] += self.size[v_rep]

    def union_by_rank(self, u, v):
        """
            merge sets using rank

            shorter tree gets attached under taller tree
            if both have same rank, attach one under the other
            and increase the new root's rank by 1
        """
        # find roots of both nodes
        u_rep = self.find(u)
        v_rep = self.find(v)

        # if both already belong to same set, nothing to merge
        if u_rep == v_rep:
            return

        # if u's tree is shorter, attach it under v's root
        if self.rank[u_rep] < self.rank[v_rep]:
            self.parent[u_rep] = v_rep
        # if v's tree is shorter, attach it under u's root
        elif self.rank[u_rep] > self.rank[v_rep]:
            self.parent[v_rep] = u_rep
        else:
            # if both trees have same rank, choose one root
            # here, attach v under u
            self.parent[v_rep] = u_rep
            # since equal-height trees were merged,
            # height of resulting tree increases by 1
            self.rank[u_rep] += 1

    def connected(self, u, v):
        """
            check if u and v belong to same set
        """
        # two nodes are connected if they have same root
        return self.find(u) == self.find(v)