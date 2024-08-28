class Solution:
    def __init__(self) -> None:
        pass
    
    def solver(self, grid):
        # get neighbors in a matrix:
        for i in range(len(grid)):
            print("\nrow " + str(i + 1) + ":")
            for j in range(len(grid[i])):
                directions = [[i - 1, j], [i, j + 1], [i + 1, j], [i, j - 1]]
                up, right, down, left = -1, -1, -1, -1
                
                if i - 1 >= 0:
                    up = grid[directions[0][0]][directions[0][1]]
                if j + 1 < len(grid[i]):
                    right = grid[directions[1][0]][directions[1][1]]
                if i + 1 < len(grid):
                    down = grid[directions[2][0]][directions[2][1]]
                if j - 1 >= 0:
                    left = grid[directions[3][0]][directions[3][1]]
                
                print("[" + str(grid[i][j]) + "]: ", end = "")
                if up != -1:
                    print(up, end = ", ")
                if right != -1:
                    print(right, end = ", ")
                if down != -1:
                    print(down, end = ", ")
                if left != -1:
                    print(left, end = "")
                    
                print("")

def main():
    solver = Solution()
    
    #solver.solver()
    print(solver.solver(grid = [[2,1,1],[1,1,0],[0,1,1]]))
    # print(solver.solver(grid = [[2,1,1],[0,1,1],[1,0,1]]))
    # print(solver.solver(grid = [[0,2]]))

if __name__ == "__main__":
    main()
