class Graph:
    def __init__(self, numNodes, edges):
        self.numNodes = numNodes
        self.edges = edges
        self.adjacencyList = [[] for _ in range(0, self.numNodes)]
        self.adjacencyMatrix = [([0] * self.numNodes) for _ in range(0, self.numNodes)]
        # the visited map is used mainly forrrrrrr DFS!
        self.DFSvisited = {}
        self.BFSvisited = []
        self.BFSqueue = []
        self.DFSTraversal = []
        self.BFSTraversal = []
    
    def addEdge(self, u, v, bidirectional = False):
        self.adjacencyList[u].append(v)
        
        if bidirectional:
            self.adjacencyList[v].append(u)
    
    def buildAdjacencyMatrix(self, edges, bidirectional = False):
        for i, j in edges:
            self.adjacencyMatrix[i][j] = 1
            if bidirectional:
                self.adjacencyMatrix[j][i] = 1
        
        for row in self.adjacencyMatrix:
            print(row)
    
    ############################## traversals #################################
    
    def dfs(self, node):
        if node in self.DFSvisited:
            return node
        
        self.DFSvisited[node] = 1
        self.DFSTraversal.append(node)

        if self.adjacencyList[node] is not None:
            for neighbor in self.adjacencyList[node]:
                self.dfs(neighbor)
        
        return node

    def bfs(self, node):
        self.BFSvisited.append(node)
        self.BFSqueue.append(node)
        
        while self.BFSqueue:
            current = self.BFSqueue.pop(0)
            self.BFSTraversal.append(current)
            
            if self.adjacencyList[current] is not None:
                for neighbor in self.adjacencyList[current]:
                    if neighbor not in self.BFSvisited:
                        self.BFSvisited.append(neighbor)
                        self.BFSqueue.append(neighbor)
        
        return self.BFSTraversal
    
    ############################## cycle detection algorithms #################################
    
    def hasCycleBFS(self, node):
        visited = set()
        
        """
            detect() is a modified BFS.
            this code is mainly for cycle detection in undirected graphs!
            for directed graphs, DFS is better.
            But in the longer run, the more the nodes, the worse recursive DFS will perform.
            So we will try to implement a better iterative DFS
        """
        def detect(node, visited):
            visited.add(node)
            
            queue = []
            # in our queue, instead of just storing the current node, we will also 
            # store the parent of the current node, sincde we wanna detect a cycle.
            # it will help to check in an indirected graph, since the parent will also be
            # in the children's neighbors' lists.
            # at the very beginning for our source node, we will add the parent as -1
            queue.append((node, -1))
            
            while queue:
                # get the current node and its parent
                current, parent = queue.pop(0)
                
                if self.adjacency_list[current] is not None:
                    for neighbor in self.adjacency_list[current]:
                        if neighbor not in visited:
                            # if it wasnt visited, add it to the visited set:
                            visited.add(neighbor)
                            # then add the neighbor and its parent (i.e. current) to the queue
                            # for further traversal:
                            queue.append((neighbor, current))
                        # if the neighbor was in visited, and if that neighbor is not the parent,
                        # that means we have found a cycle!
                        elif neighbor != parent:
                            return True
                        # if that neighbor is the parent, then we can just keep processing the queue

            return False

        # now we have to run detect() through all the nodes in the
        # adjacency list - unless they're visited (obviously)
        # because the graph can also have other disjoint components
        # that might or might not have cycles:
        for i in range(len(self.adjacency_list)):
            if i not in visited:
                if detect(i, visited):
                    return True
        
        return False
    
    def hasCycleDFS(self, node):
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
        for node in range(len(self.adjacencyList)):
            print(node, end = ": ")
            print(self.adjacencyList[node])
    

def main():
    edges = [[0, 1], [0, 2], [1, 3], [2, 3], [4, 2], [4, 5]]
    graph1 = Graph(6, edges)
    
    for edge in edges:
        graph1.addEdge(edge[0], edge[1], bidirectional=True)
    
    graph1.printGraph()
    
    graph1.dfs(0)
    print(graph1.DFSTraversal)
    
    print(graph1.bfs(0))

if __name__ == "__main__":
    main()
