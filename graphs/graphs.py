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