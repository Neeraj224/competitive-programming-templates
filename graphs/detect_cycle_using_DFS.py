class Graph:
    def __init__(self, numNodes, edges, adjacency_list):
        self.numNodes = numNodes
        self.edges = edges
        
        # self.adjacency_list = [[] for _ in range(0, self.numNodes)]
        self.adjacency_list = adjacency_list
        self.BFSTraversal = []
        self.BFSVisited = []
        self.BFSQueue = []
        
        self.DFSVisited = {}
        self.DFSTraversal = []
    
    def addEdge(self, u, v, bidirectional = False):
        self.adjacency_list[u].append(v)
        
        if bidirectional:
            self.adjacency_list[v].append(u)
    
    def dfs(self, node):
        if node in self.DFSVisited:
            return node
        
        self.DFSTraversal.append(node)
        self.DFSVisited[node] = 1
        
        if self.adjacency_list[node] is not None:
            for neighbor in self.adjacency_list[node]:
                self.dfs(neighbor)
        
        return node
                
    
    def bfs(self, node):
        self.BFSTraversal = []
        self.BFSVisited = []
        self.BFSQueue = []
        
        self.BFSVisited.append(node)
        self.BFSQueue.append(node)
        
        while self.BFSQueue:
            current = self.BFSQueue.pop(0)
            
            self.BFSTraversal.append(current)
            
            if self.adjacency_list[current] is not None:
                for neighbor in self.adjacency_list[current]:
                    if neighbor not in self.BFSVisited:
                        self.BFSVisited.append(neighbor)
                        self.BFSQueue.append(neighbor)
        
        return self.BFSTraversal
    
    def hasCycle(self, node):
        # this hasCycle() detection method will use DFS, instead of the previous one we used - BFS
        # DFS helps in finding cycles in directed graphs, while BFS is comparatively better for
        # undirected graphs.
        
        visited = set()
        
        def dfs(node, parent):
            # first we will add the current node to the visited set:
            visited.add(node)
            
            # then check if it has neighbors
            if self.adjacency_list[node] is not None:
                # if it does, then we iterate over the neighbors one by one, 
                # performing dfs on all of them, and checking if we encountered a node
                # again - but a node that isnt the parent of the current one we're visiting!
                for neighbor in self.adjacency_list[node]:
                    # so lets see first if it was visited or not:
                    if neighbor not in visited:
                        # if it wasnt, then call dfs on its neighbor recursively (if it wasnt visited)
                        # and check if it returns True or not
                        if dfs(neighbor, node) == True:
                            # if it does, then somewhere down the branch, it detected a cycle
                            # so we already got a cycle, then we need to return True
                            return True
                    # else if it was visited, and the neighbor isnt a parent,
                    # then it means it found a visited node before - that means
                    # we ended up traversing to somewhere we had already crossed.
                    # That means we have a cycle!
                    # (this will be our base case btw):
                    elif neighbor != parent:
                        # so return True:
                        return True
            
            # or if we never encounter a node twice (even until a certain branch), that means
            # there was no cycle, so we just return False:
            return False
        
        for i in range(0, len(self.adjacency_list)):
            if i not in visited:
                if dfs(i, -1) == True:
                    return True
        
        return False
             
        
    def printGraph(self):
        for node in range(len(self.adjacency_list)):
            print("[" + str(node) + "]: " + str(self.adjacency_list[node]))

def main():
    adjl1 = [[1], [0, 2, 4], [1, 3], [2, 4], [1, 3]]
    edges = []
    
    graph1 = Graph(5, edges, adjacency_list = adjl1)
    
    graph1.printGraph()
    graph1.bfs(0)
    graph1.dfs(0)
    
    print(graph1.BFSTraversal)
    print(graph1.DFSTraversal)
    
    print(graph1.hasCycle(0))
    
    adjl2 = [[], [2], [1, 3], [2]]
    edges = []
    graph2 = Graph(4, edges, adjacency_list = adjl2)
    
    print(graph2.hasCycle(0))
        
    
if __name__ == "__main__":
    main()