class Solution:
    def __init__(self) -> None:
        pass
    
    def solver(self, mat):
        # pass
        distances_mat = [([0] * len(mat[0])) for _ in range(len(mat))]
        visited = [([float("-inf")] * len(mat[0])) for _ in range(len(mat))]
        
        queue = []
        
        for i in range(len(mat)):
            for j in range(len(mat[0])):
                if mat[i][j] == 0:
                    queue.append((i, j, 0))
                    visited[i][j] = 1
                    
        distances = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        while queue:
            row, col, distance = queue.pop(0)
            distances_mat[row][col] = distance
            
            for dx, dy in distances:
                new_x = row + dx
                new_y = col + dy
                if 0 <= new_x < len(mat) and 0 <= new_y < len(mat[0]) and visited[new_x][new_y] == float('-inf'):
                    visited[new_x][new_y] = 1
                    queue.append((new_x, new_y, distance + 1))
        
        return distances_mat

def main():
    solver = Solution()
    
    #solver.solver()
    print(solver.solver(mat = [[0,0,0],[0,1,0],[0,0,0]]))
    print(solver.solver(mat = [[0,0,0],[0,1,0],[1,1,1]]))
    # print(solver.solver())

if __name__ == "__main__":
    main()