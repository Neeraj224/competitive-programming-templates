class Stack:
    def __init__(self):
        self._stack = []
    
    def push(self, item):
        self._stack.append(item)
        
    def pop(self):
        popped = self._stack[-1]
        self._stack.remove(self._stack[-1])
        return popped

    def peek(self):
        if self.isempty():
            print("stack is empty")
            return
        
        return self._stack[-1]

    def size(self):
        return len(self._stack)

    def isempty(self):
        if self.size() == 0:
            return True
        
        return False
    
def main():
    st1 = Stack()
    print(st1.isempty())
    st1.peek()
    st1.push(10)
    st1.push(20)
    print(st1.peek())
    print(st1.size())
    print(st1.pop())
    print(st1.peek())
    print(st1.size())

if __name__ == "__main__":
        main()
    
