from collections import deque

class Solution:
    def __init__(self) -> None:
        pass
    
    def solver(self, grid, sx, sy):
        # pass
        # direction vectors:
        # up, right, down, left 
        dRow = [-1, 0, 1, 0]
        dCol = [0, 1, 0, -1]
        
        visited = [[False for i in range(len(grid[0]))] for i in range(len(grid))]
        
        BFSMatrixTraversal = []
        
        def isValid(row, col, n, visited):
            # if cell lies out of bounds:
            if row < 0 or col < 0 or row >= n or col >= n:
                return False

            # if the cell has already been visited:
            if visited[row][col]:
                return False

            # otherwise, its a valid cell:
            return True

        queue = deque()
        
        queue.append((sx, sy))
        visited[sx][sy] = True
        
        while queue:
            current = queue.popleft()
            x = current[0]
            y = current[1]
            # print(grid[x][y], end = " ")
            BFSMatrixTraversal.append(grid[x][y])
            
            # now we check the adjacent cells:
            for i in range(4):
                adjX = x + dRow[i]
                adjY = y + dCol[i]
                
                if isValid(adjX, adjY, len(grid), visited):
                    queue.append((adjX, adjY))
                    visited[adjX][adjY] = True
        
        return BFSMatrixTraversal


def main():
    solver = Solution()
    grid = [ [ 1, 2, 3, 4 ],
		     [ 5, 6, 7, 8 ],
		     [ 9, 10, 11, 12 ],
		     [ 13, 14, 15, 16 ] ]
    
    print(solver.solver(grid, 0, 0))
    # print(solver.solver())
    # print(solver.solver())

if __name__ == "__main__":
    main()