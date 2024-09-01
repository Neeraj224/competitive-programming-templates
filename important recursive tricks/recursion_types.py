class MasterFunction:
    def __init__(self) -> None:
        # pass
        self.visited = []
        self.namecount = 5
    
    def name(self, str):
        # our base case
        if self.namecount == 0:
            return
        
        # the processing
        print("hi, " + str)
        # decrementing step
        self.namecount -= 1
        
        # calling it recursively
        self.name(str)
    
    def _12N_(self, current, n):
        if current == n + 1:
            return

        print(current)
        current += 1
        
        self._12N_(current, n)
    
    def _N21_(self, current):
        if current == 0:
            return
        
        print(current)
        
        self._N21_(current - 1)
    
    # the follwing is backtracking, 
    # because we go till n, and then while backtracking, we start
    # processing (in this case jsut simple printing) and keep returning
    def backtrackN(self, n):
        if n != 1:
            self.backtrackN(n - 1)
        print(n)
        
    def backtrack1(self, i, n):
        if i != n:
            self.backtrack1(i + 1, n)
        print(i)
    
    # basic 1D DP for to find a sum of first n numbers
    def sumN(self, n):
        # normal summing, the dp recursion way:
        arr = [0] * (n + 1)
        arr[0] = 0
        
        def recurse(n):
            if n != 1:
                recurse(n - 1)
            arr[n] = n + arr[n - 1]
        
        recurse(n)
        # print(arr)
        return arr[-1]
        
    # another way for recursion:
    def sumNN(self, n):
        # this is parameterised recursion:
        def recurse(n, sum):
            # until we reach the end, i.e. 0,
            # keep recursing and adding to the parameter
            if n != 0:
                recurse(n - 1, sum + n)
            # one we're there, just start printing
            print(sum)
        
        recurse(n, 0)

        # we can also do this using basic dp tabulation:
        dp_arr = [0] * (n + 1)
        
        def dp(n, sum):
            if n != 0:
                dp(n - 1, sum + n)
            # instead of printing, just save it at the nth
            # index and then check the table
            # after the function is done running
            dp_arr[n] = sum
        
        dp(n, 0)
        
        # print(dp_arr) -> we know our sum will be at the very front:
        # so we return the first index:
        return dp_arr[0]
            
    # the following way of recursion is the functional way:
    # all you have to do is, just require the base case
    def f(self, n):
        if n == 0:
            return 0
        else:
            return n + self.f(n - 1)

def main():
    mf = MasterFunction()
    
    # mf.name("neemu")
    # mf.name("keemu") 
    # mf._12N_(1, 10)
    # mf._N21_(10)
    # mf.backtrackN(10)
    # mf.backtrack1(1, 10)
    
    # print(mf.sumN(5))
    # print(mf.sumNN(5))
    print(mf.f(5))
    
    
if __name__ == "__main__":
    main()