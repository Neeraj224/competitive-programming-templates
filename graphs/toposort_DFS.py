class Graph:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        self.adjacencyList = [[] for _ in range(self.nodes)]
        self.indegrees = [0] * self.nodes
    
    def addEdges(self):
        # pass
        for edge in self.edges:
            self.adjacencyList[edge[0]].append(edge[1])
    
    def getIndegrees(self):
        for edge in self.edges:
            self.indegrees[edge[1]] += 1

    def printGraph(self):
        print(self.adjacencyList)

class Solution:
    def __init__(self) -> None:
        pass
    
    def solver(self, nodes, edges):
        # pass
        graph = Graph(nodes, edges)
        graph.addEdges()
        
        # topological sort using DFS:
        visited = [0] * nodes
        stack = []
        
        def dfs(node):
            # mark the node as visited
            visited[node] = 1
            
            if graph.adjacencyList[node] is not None:
                for neighbor in graph.adjacencyList[node]:
                    # if it hasnt been visited
                    if visited[neighbor] == 0:
                        # perform DFS on it:
                        dfs(neighbor)
            
            # and after its done, append it to the stack
            stack.append(node)
        
        # do this for all the components of the graph:
        for i in range(nodes):
            if visited[i] == 0:
                dfs(i)
        
        ordering = []
        
        # get the order from the stack
        while stack:
            ordering.append(stack.pop())
        
        # return the topological order!
        return ordering                        
                 

def main():
    solver = Solution()
    
    #solver.solver()
    print(solver.solver(nodes = 4, edges = [[1, 0], [2, 0], [3, 0]]))
    print(solver.solver(nodes = 6, edges = [[1, 3], [2, 3], [4, 0], [4, 1], [5, 0], [5, 2]]))
    # print(solver.solver())

if __name__ == "__main__":
    main()