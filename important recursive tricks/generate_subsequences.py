class Solution:
    def __init__(self) -> None:
        pass
    
    def solver(self, arr):
        # pass
        subsequences = []
        
        # a very simple backtracking way of getting subsequences:
        def get_sequences(i, current):
            # this is our base case:
            if i == len(arr):
                # at the last index, we need to process/
                # or get the element or whatever for the last time
                # once - so that we dont lose it
                if current not in subsequences:
                    subsequences.append(current.copy())
                # and then end our recursion
                return
             
             # now, if it isnt present in the subsequences:
            if current not in subsequences:
                # add it:
                subsequences.append(current.copy())
            
            # there are two ways for backtracking and DP:
            # we usually do two things: TAKE or NOT TAKE
            # this step is the TAKE step:
            current.append(arr[i])
            # then after taking lets further explore this branch until
            # we find a base case:
            get_sequences(i + 1, current) 
            
            # after the previous branch is done being explored, we go to
            # a different branch - this is the NOT TAKE step:
            # this is how we also backtrack:
            # so pop it:
            current.pop()
            # and go to the next branch:
            get_sequences(i + 1, current)
            
        # call the recursive function:
        get_sequences(0, [])
        
        return subsequences

def main():
    solver = Solution()
    
    #solver.solver()
    print(solver.solver([3, 1, 2]))
    print(solver.solver([0, 4, 5, 1]))
    # print(solver.solver())

if __name__ == "__main__":
    main()