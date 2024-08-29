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
    
    def hasCycle(self, node):
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
