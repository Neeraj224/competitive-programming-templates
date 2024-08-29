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
        visited = set()
        
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