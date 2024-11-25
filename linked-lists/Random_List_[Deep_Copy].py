"""
    Template for the Linked List questions on Leetcode.
    I have added basic methods like:
        - building the list from an array
        - getting the length of the list
        - printing the list
        - getting the next node of a node
"""
class ListNode:
    def __init__(self, val = 0, next = None):
        self.val = val
        self.next = None
    
    def printListFromNode(self, head):
        """
            This method is for lists we need to print directly
            from the node. Because we cannot use another list's
            object to randomly pass a node for some other list
            just to print it.
        """
        if head == None:
            return []
        
        current = head
        
        print("[", end = "")
        while current:
            print(current.val, end = " -> ")
            current = current.next
        print("None]")
        
class LinkedList:
    def __init__(self):
        self.head = None
    
    def buildList(self, elements):
        if len(elements) == 0:
            return self.head
        
        current = ListNode(elements[0])
        self.head = current
        
        for i in range(1, len(elements)):
            current.next = ListNode(elements[i])
            current = current.next
        
        return self.head

    def getListLength(self):
        if self.head == None:
            return 0
        
        current = self.head
        numElements = 0
        
        while current:
            numElements += 1
            current = current.next
        
        return numElements
    
    def printList(self):
        if self.head == None:
            return []
        
        current = self.head
        
        print("[", end = "")
        while current:
            print(current.val, end = " -> ")
            current = current.next
        print("None]")
    
    def findNext(self, val):
        current = self.head
        
        while current and current.val != val:
            current = current.next
        
        if not current:
            return "Node not found!"
        
        if current.next:
            return current.next.val
        else:
            print("There's nothing at the end of this node!")
            return None

######################################################################

"""
    DEFINING A RANDOM LIST:
"""

######################################################################

"""
    Have to write a different definition for the node of this linked list
    because it has random pointers as well.
"""
class Node:
    """
        Each node is represented as a pair of [val, random_index] where:
            - val: an integer representing Node.val
            - random_index: the index of the node (range from 0 to n-1) that 
              the random pointer points to, or null if it does not point to any node.
    """
    def __init__(self, val = 0, next = None, random = None):
        self.val = val
        self.next = next
        self.random = random
    
    def buildRandomList(self, structure):
        # first we build the list with its straight next pointers:        
        if len(structure) == 0:
            return None
        
        current = Node(val = structure[0][0], random = structure[0][1])
        randomHead = current
        
        for i in range(1, len(structure)):
            # current.next = Node(val = structure[i][0], random = structure[i][1])
            current.next = Node()
            current.next.val = structure[i][0]
            current.next.random = structure[i][1]
            # print(current.val)
            # print(current.random)
            current = current.next
        
        # now that our list has been built with its next pointers,
        # we need to assign the random pointers.
        
        current = randomHead
        rTraverse = randomHead
        
        while current:
            randomIndex = current.random
            currentRandom = 0
            
            if randomIndex == None:
                while rTraverse:
                    rTraverse = rTraverse.next
                current.random = rTraverse
            else:
                while randomIndex != currentRandom and rTraverse:
                    rTraverse = rTraverse.next
                    currentRandom += 1
                current.random = rTraverse
            
            rTraverse = randomHead
            current = current.next
        
        return randomHead
    
    def printRandomList(self, head):
        if head is None:
            return None
        
        current = head
        
        print("[ ", end = "")
        while current:
            print("[", end = "")
            print(current.val, end = " | ")
            if current.random is None:
                print("None", end = "] -> ")
            else:
                print(current.random.val, end = "] -> ")
            current = current.next
        print(" ]")

####################################################################

class Solution:
    def __init__(self):
        # pass
        self.hashedStorage = {None: None}
    
    def solver(self, head):
        # pass
        # first we initialize a current pointer
        current = head
        
        # next we traverse through the list, creating copies of the nodes
        # using their values. then we store these copies in our hashStorage
        # by hashing the original nodes
        while current:
            copy = Node(current.val)
            self.hashedStorage[current] = copy
            current = current.next
        
        # once all the nodes have been created using their values.
        # it's easy to just update the pointers!
        # so, now we reinitialize our current, and this time, we will
        # update the pointers to the copies (copied nodes), by hashing
        # the nodes' pointers!
        current = head
        
        while current:
            copy = self.hashedStorage[current]
            copy.next = self.hashedStorage[current.next]
            copy.random = self.hashedStorage[current.random]
            current = current.next
        
        deepCopy = self.hashedStorage[head]
        
        return deepCopy        
        

####################################################################

def main():
    structure = [[7, None], [13, 0], [11, 4], [10,2], [1,0]]
    randomList = Node()
    randomList = randomList.buildRandomList(structure = structure)
    randomList.printRandomList(head = randomList)
    
    solver = Solution()
    deepCopy = solver.solver(head = randomList)
    deepCopy.printRandomList(head = deepCopy)
   
    # listOne.printList()
    # print(listOne.findNext(2))
    # print(listOne.findNext(5))
    # print(listOne.findNext(8))
    # print(listOne.getListLength())

if __name__ == "__main__":
    main()