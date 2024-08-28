class Solution:
    def __init__(self) -> None:
        pass
    
    def solver(self, image, sr, sc, color):
        prev_color = image[sr][sc]

        if prev_color == color:
            return image
        
        def dfs(row, col):
            if image[row][col] == prev_color:
                image[row][col] = color

                if row - 1 >= 0:
                    # up
                    dfs(row - 1, col)
                if col + 1 < len(image[0]):
                    # right
                    dfs(row, col + 1)
                if row + 1 < len(image):
                    # down
                    dfs(row + 1, col)
                if col - 1 >= 0:
                    # left
                    dfs(row, col - 1)
        
        dfs(sr, sc)
        
        return image

def main():
    solver = Solution()
    
    #solver.solver()
    print(solver.solver(image = [[1,1,1],[1,1,0],[1,0,1]], sr = 1, sc = 1, color = 2))
    print(solver.solver(image = [[0,0,0],[0,0,0]], sr = 0, sc = 0, color = 0))
    # print(solver.solver(grid = [[0,2]]))

if __name__ == "__main__":
    main()
