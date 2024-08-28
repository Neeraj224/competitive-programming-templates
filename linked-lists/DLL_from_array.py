class ListNode:
    def __init__(self, val) -> None:
        self.val = val
        self.next = None
        self.prev = None

def create(arr):
    head = ListNode(arr[0])
    current = head
    
    for i in range(1, len(arr)):
        current.next = ListNode(arr[i])
        current.next.prev = current
        current = current.next
    
    return head
    
def printList(head):
    current = head
    
    print("[ ", end = "")
    while current:
        print(current.val, end = " <=> ")
        current = current.next
    print("None ]")
    
def printReverse(head):
    current = head
    
    while current.next != None:
        current = current.next
    
    print("[ None", end = "")
    while current:
        print(" <=> ", end = "")
        print(current.val, end = "")
        current = current.prev
    print(" ]")

def insert(head, pos, val):
    current = head
    insert_pos = 0
    
    while current:
        # case 1: inserting at the tail
        if current.next == None:
            newListNode = ListNode(val)

            current.next = newListNode
            newListNode.prev = current
            
            return head
        
        # case 2: inserting anywhere else:
        if insert_pos == pos:
            # insert
            newListNode = ListNode(val)
            
            # shuffle pointers:
            newListNode.next = current.next
            newListNode.prev = current
            current.next = newListNode
            newListNode.next.prev = newListNode
            
            return head
        else:
            insert_pos += 1
            current = current.next
        
    return False

def delete(head, pos):
    curr_pos = 1 
    current = head
    
    # case 1: if deleting at head
    if pos == 1:
        head = current.next
        head.prev.next = None
        head.prev = None
        return head
    
    # traverse the list to get to the position:
    while pos != curr_pos:
        current = current.next
        curr_pos += 1
    
    # case 2: if deleting at the tail:
    if current.next == None:
        current.prev.next = None
        current.prev = None
    # case 3: if deleting anywhere else:
    else:
        current.prev.next = current.next
        current.next.prev = current.prev
        current.next = None
        current.prev = None
    
    return head

def length(head):
    length = 0
    current = head
    
    while current:
        length += 1
        current = current.next
    
    return length

# Code for reversing a linked list:
def reverseList(head):
    current = head
    
    left = current
    right = current
    length = 1
    
    while right.next != None:
        right = right.next
        length += 1
    
    print(right.val)
    
    if length % 2 == 1:
        middle = length // 2 + 1
    else:
        middle = length // 2
    
    i = 0
    
    while i < middle:
        left.val, right.val = right.val, left.val
        
        left = left.next
        right = right.prev
        
        i += 1
    
    return head

def main():
    # driver code
    dll1 = create([1, 2, 3, 4, 5])
    printList(dll1)
    printReverse(dll1)
    
    dll2 = create([1, 2, 3, 4, 5])
    printList(dll2)
    
    # delete head:
    dll2 = delete(dll2, 1)
    printList(dll2)
    # delete anywhere else:
    dll2 = delete(dll2, 4)
    printList(dll2)
    # delete tail:
    dll2 = delete(dll2,3)
    printList(dll2)

if __name__ == "__main__":
    main()