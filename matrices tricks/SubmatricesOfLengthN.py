class Solution:
    def __init__(self) -> None:
        pass
    
    def solver(self, grid):
        # pass
        def print3x3SubMatrix(grid, windowSize):
            for i in range(0, len(grid) - (windowSize - 1)):
                for j in range(0, len(grid[i]) - (windowSize - 1)):
                    print("---------------")
                    for k in range(i, i + windowSize):
                        print("[ ", end = "")
                        for l in range(j, j + windowSize):
                            print(grid[k][l], end = " ")
                        print("]")
        
        print3x3SubMatrix(grid, 3)
        print3x3SubMatrix(grid, 2)
        print3x3SubMatrix(grid, 4)
        

def main():
    solver = Solution()
    
    #solver.solver()
    print(solver.solver(grid = [[9,9,8,1],[5,6,2,6],[8,2,6,4],[6,2,2,2]]))
    print(solver.solver(grid = [[1,1,1,1,1],[1,1,1,1,1],[1,1,2,1,1],[1,1,1,1,1],[1,1,1,1,1]]))
    # print(solver.solver())

if __name__ == "__main__":
    main()