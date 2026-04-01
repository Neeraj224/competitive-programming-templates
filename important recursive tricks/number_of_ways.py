# check this question: https://codeforces.com/group/MWSDmqGsZm/contest/223339/problem/Y

import sys
input = sys.stdin.readline

def solve():
    start, end = map(int, input().split())
    
    def recurse(i):
        if i == end:
            return 1
        if i > end:
            return 0
        
        return (
            recurse(i + 1) +
            recurse(i + 2) +
            recurse(i + 3)
        )
    
    return recurse(start)

def solve_generate_paths():
    start, end = map(int, input().split())
    """
        write code here!
    """
    result = []
    
    # we append the initial start to our path:
    path = [start]
    
    def recurse(i):
        # nonlocal to maintain the state:
        nonlocal path
        
        # if we reach the end
        if i == end:
            # add our path found to the resulting array
            result.append(path.copy())
            # and simply prune this branch
            return
        if i > end:
            # if we have gone beyond our end
            # just prune the branch
            return
        
        # now, we need to look from i + 1 to i + 3
        for x in range(1, 4):
            # if i + x is below our end, only then explore
            if i + x <= end:
                # append the path
                path.append(i + x)
                # recursively explore
                recurse(i + x)
                # and pop it
                path.pop()
        
        """even appending the paths, and popping would work:
        take the path with +1:"""
        # path.append(i + 1)
        """recursively explore:"""
        # recurse(i + 1)
        """and then clear it so we can move with the next"""
        # path.pop()
        
        """now append the path with +2 steps"""
        # path.append(i + 2)
        """explore:"""
        # recurse(i + 2)
        """pop:"""
        # path.pop()
        
        """same with the last step, append the one with +3 steps"""
        # path.append(i + 3)
        """explore"""
        # recurse(i + 3)
        """remove"""
        # path.pop()
        
        return

    recurse(start)
    
    return result
    
def main():
    # t = int(input())  # uncomment if multiple test cases
    print(solve())

if __name__ == "__main__":
    main()
