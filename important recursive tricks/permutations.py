class Solution:
    def __init__(self) -> None:
        pass
    
    def solver(self, nums):
        # pass
        result = []
        n = len(nums)
        map = [0] * n 
        
        def backtrack(current, map):
            if len(current) == n:
                result.append(current[:])
                return
            
            for i in range(n):
                if not map[i]:
                    map[i] = 1
                    current.append(nums[i])
                    backtrack(current, map)
                    current.pop()
                    map[i] = 0
        
        backtrack([], map)
        
        return result

def main():
    solver = Solution()
    
    #solver.solver()
    print(solver.solver([1, 2, 3]))
    print(solver.solver([0, 1]))
    # print(solver.solver())

if __name__ == "__main__":
    main()