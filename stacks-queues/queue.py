"""
    insert at tail, delete from head.
"""
class Queue:
    def __init__(self):
        self._queue = list()
        self._capacity = 100005
        self._head = 0
        self._tail = 0
    
    def enqueue(self, item):
        if self.size() >= self._capacity:
            return "Queue is full"
        
        self._queue.append(item)
        self._tail += 1
        return

    def dequeue(self):
        if self.size() <= 0:
            self.reset()
            return -1
        
        dequeued = self._queue[self._head]
        self._head += 1
        
        return dequeued
    
    def size(self):
        return self._tail - self._head
    
    def reset(self):
        self._tail, self._head = 0, 0
        self._queue = list()
        
def main():
    q1 = Queue()
    print(q1.size())
    q1.enqueue(21)
    q1.enqueue(22)
    q1.enqueue(24)
    q1.enqueue(25)
    print(q1.size())
    print(q1.dequeue()) # should give 21 because that was added first!
    print(q1.size())
    
if __name__ == "__main__":
        main()
    