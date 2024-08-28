"""
    Singly Linked List from an array and operations:
"""
class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None

def constructFromArray(arr):
    current = ListNode(arr[0])
    head = current
    
    for i in range(1, len(arr)):
        current.next = ListNode(arr[i])
        current = current.next
    
    return head

def printList(head):
    current = head
    print("[", end = " ")
    while current:
        print(current.val, end = " -> ")
        current = current.next
    
    print(None, end = " ]")
    print("")

# append a ListNode to the end of the linked list
def append(listHead, val):
    # if the linked list is empty:
    if not listHead:
        return ListNode(val)
        
    current = listHead
        
    # find the one with the next pointer as None (Null)
    while current.next != None:
        current = current.next
    # and create a ListNode with the current's next pointer pointing to it:
    current.next = ListNode(val)
        
    return listHead

def delete(head, target):
    curr = head
    
    while curr.next.val != target:
        curr = curr.next
    
    # get the one to be deleted in a temp variable
    deleted = curr.next
    # update pointer of the previous ListNode to the next to the one being deleted:
    curr.next = curr.next.next
    # update pointer of the one to be deleted to None
    deleted.next = None
    
    return head

def getLength(head):
    length = 0
    current = head
    
    while current:
        length += 1
        current = current.next
    
    return length

def search(head, key):
    current = head
    
    while current:
        if current.val == key:
            return True
        current = current.next
    
    return False


def createCopyOfList(head):
    copy = ListNode()
    currentCopy = copy
    
    if not head:
        copy = head
        return copy
    
    current = head
    
    while current:
        currentCopy.next = ListNode(current.val)
        current = current.next
        currentCopy = currentCopy.next
    
    copy = copy.next
    return copy

def main():
    # driver code
    list1 = constructFromArray(arr = [1, 2, 3, 4, 5])
    list2 = constructFromArray(arr = [2, 4, 6, 7, 5, 1, 0])
    
    printList(list1)
    printList(list2)
    
    list1 = append(list1, 10)
    printList(list1)
    
    list1 = delete(list1, 3)
    printList(list1)
    
    print(getLength(list1))
    
    print(search(list1, 4))
    print(search(list1, 3))
    print(search(list1, 10))
    print(search(list2, 7))
    
    
if __name__ == "__main__":
    main()