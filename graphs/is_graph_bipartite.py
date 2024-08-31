class Solution:
    def __init__(self) -> None:
        pass
    
    def solver(self, graph):
        # pass
        colors = [0] * len(graph)
        
        def dfs(node, color):
            if colors[node]:
                return colors[node] == color
            
            colors[node] = color
            
            if graph[node] is not None:
                for neighbor in graph[node]:
                    if not dfs(neighbor, -color):
                        return False

            return True
        
        for i in range(len(graph)):
            if not colors[i] and not dfs(i, 1):
                return False

        return True

def main():
    solver = Solution()
    
    #solver.solver()
    print(solver.solver(graph = [[1,2,3],[0,2],[0,1,3],[0,2]]))
    print(solver.solver(graph = [[1,3],[0,2],[1,3],[0,2]]))
    # print(solver.solver())

if __name__ == "__main__":
    main()