from collections import defaultdict

"""
================================================================================
MAIN IDEA for LFU Cache:

We are designing a cache where eviction is based on:
    1) Least Frequently Used (LFU)
    2) If frequencies tie => Least Recently Used (LRU)

To achieve O(1) operations for both get() and put(), we use:

    1) nodeMap:
        key => node
        This helps us directly access any node in O(1)

    2) listMap:
        freq => Doubly Linked List of nodes
        Each frequency has its own list

    3) lfuCnt:
        This tracks the minimum frequency currently present in the cache
        This helps us know from which list we should evict

--------------------------------------------------------------------------------
STRUCTURE:

Suppose we have:

    freq = 1 => [ 2 <-> 5 <-> 7 ]
    freq = 2 => [ 1 <-> 9 ]
    freq = 3 => [ 3 ]

Each list is a Doubly Linked List:

    LEFT  => Least Recently Used (LRU)
    RIGHT => Most Recently Used (MRU)

So when eviction happens:
    - we look at lfuCnt (say = 1)
    - we remove from LEFT of that list (LRU among LFU)

--------------------------------------------------------------------------------
OPERATIONS:

get(key):
    - if key exists:
        - increase frequency
        - move node to new frequency list
    - else return -1

put(key, value):
    - if key exists:
        - update value
        - increase frequency
    - else:
        - if capacity full:
            - evict from lfuCnt list (popLeft)
        - insert new node with freq = 1
        - update lfuCnt = 1

================================================================================
"""


class ListNode:
    def __init__(self, key, val):
        """
            This node represents a single key-value entry in the LFU cache.

            Each node stores:
            - key => so that we can remove it from nodeMap during eviction
            - value => the actual data associated with this key
            - frequency => number of times this key has been accessed
        """
        # We store the key because during eviction we only have the node,
        # and we need to remove the corresponding entry from nodeMap in O(1)
        self.key = key
        # We store the value so that get() can return it directly
        self.val = val
        # Every new node starts with frequency = 1
        # because inserting a key counts as one usage
        self.freq = 1
        # This pointer will point to the previous node in the linked list
        # and is required for O(1) removal
        self.prev = None
        # This pointer will point to the next node in the linked list
        # and is required for O(1) insertion and traversal
        self.next = None


class LinkedList:
    def __init__(self):
        """
            This linked list stores nodes that all have the same frequency.

            We use a doubly linked list because:
            - we need O(1) insertion
            - we need O(1) deletion from anywhere

            The structure is:
                left <-> ...nodes... <-> right

            Where:
                left.next  => Least Recently Used (LRU)
                right.prev => Most Recently Used (MRU)
        """
        # We create a dummy left node to act as a boundary.
        # This helps us avoid edge case checks during insertion/removal.
        self.left = ListNode(0, 0)
        # We create a dummy right node to act as a boundary.
        # This represents the end of the list.
        self.right = ListNode(0, 0)
        # Initially, the list is empty, so left connects directly to right.
        self.left.next = self.right
        # Similarly, right connects back to left.
        self.right.prev = self.left
        # We maintain the size of the list so that we can quickly check
        # whether a frequency bucket becomes empty.
        self.size = 0

    def length(self):
        """
            This function returns the number of real nodes in the list.
            It does not count the dummy left and right nodes.
        """
        return self.size

    def pushRight(self, node):
        """
            This function inserts a node at the RIGHT side of the list.

            This means:
            - the node becomes the Most Recently Used (MRU) within this frequency.
        """
        # We first identify the current last real node,
        # which is the node just before the dummy right node.
        prev = self.right.prev

        # We connect that last node to our new node.
        # This inserts the new node after prev.
        prev.next = node

        # We set the new node’s previous pointer to prev,
        # so that the backward link is maintained.
        node.prev = prev

        # We connect the new node to the dummy right node.
        # This ensures the forward link is maintained.
        node.next = self.right

        # We update the dummy right node’s previous pointer
        # so that it now points to the new node.
        self.right.prev = node

        # Since we have successfully added a node,
        # we increment the size of this list.
        self.size += 1

    def pop(self, node):
        """
            This function removes a given node from the list.

            Since we already have a reference to the node,
            we can remove it in O(1) time.
        """
        # We fetch the node before the current node.
        prev = node.prev
        # We fetch the node after the current node.
        next = node.next

        # We connect the previous node directly to the next node.
        # This effectively removes the current node from the list.
        prev.next = next
        # We also connect the next node back to the previous node.
        # This completes the bidirectional unlinking.
        next.prev = prev

        # We clear the node’s own pointers.
        # This is not strictly necessary, but helps avoid bugs.
        node.prev = None
        node.next = None

        # Since we removed a node, we decrement the size.
        self.size -= 1

    def popLeft(self):
        """
            This function removes the Least Recently Used node.

            The LRU node is always the node immediately after the dummy left node.
        """
        # If the list has no real nodes, we cannot remove anything.
        if self.length() == 0:
            return None

        # The LRU node is the first real node in the list.
        node = self.left.next
        # We remove this node using the pop() function.
        self.pop(node)

        # We return the removed node so that the caller can handle eviction.
        return node


class LFUCache:
    def __init__(self, capacity: int):
        """
            This initializes the LFU cache.

            We maintain:
            - nodeMap => key => node
            - listMap => frequency => linked list
            - lfuCnt  => minimum frequency currently present
        """
        # This stores the maximum number of elements the cache can hold.
        self.cap = capacity
        # This stores the current minimum frequency in the cache.
        # It helps us decide which nodes to evict.
        self.lfuCnt = 0
        # This map allows us to access any node directly using its key.
        self.nodeMap = {}
        # This map groups nodes by their frequency.
        # Each frequency points to a linked list.
        self.listMap = defaultdict(LinkedList)

    def counter(self, node):
        """
            This function increases the frequency of a node.

            Steps:
            - remove node from current frequency list
            - update lfuCnt if needed
            - increase frequency
            - insert into new frequency list
        """
        # We store the current frequency of this node.
        cnt = node.freq

        # We remove the node from its current frequency list.
        self.listMap[cnt].pop(node)

        # If this node belonged to the minimum frequency
        # and removing it makes that list empty,
        # we must increase lfuCnt.
        if cnt == self.lfuCnt and self.listMap[cnt].length() == 0:
            self.lfuCnt += 1

        # We increment the node’s frequency.
        node.freq += 1

        # We insert the node into the new frequency list.
        self.listMap[node.freq].pushRight(node)

    def get(self, key: int) -> int:
        """
            This function returns the value for a key if it exists.

            It also updates the frequency of that key.
        """
        # If the key is not present in the cache,
        # we return -1 as specified.
        if key not in self.nodeMap:
            return -1

        # We fetch the node corresponding to this key.
        node = self.nodeMap[key]
        # Since this key is accessed, we increase its frequency.
        self.counter(node)

        # We return the value stored in the node.
        return node.val

    def put(self, key: int, value: int) -> None:
        """
            This function inserts or updates a key in the cache.

            It also handles eviction when the cache is full.
        """
        # If capacity is zero, we cannot store anything.
        if self.cap == 0:
            return

        # If the key already exists, we update its value
        # and increase its frequency.
        if key in self.nodeMap:
            node = self.nodeMap[key]
            node.val = value
            self.counter(node)
            return

        # If the cache is full, we must evict one node.
        if len(self.nodeMap) == self.cap:
            # We remove the LRU node from the minimum frequency list.
            node = self.listMap[self.lfuCnt].popLeft()
            # We remove that node from nodeMap using its key.
            self.nodeMap.pop(node.key)

        # We create a new node for this key-value pair.
        node = ListNode(key, value)

        # We insert this node into nodeMap for O(1) access.
        self.nodeMap[key] = node
        # We insert this node into the frequency = 1 list.
        self.listMap[1].pushRight(node)

        # Since we inserted a new node with frequency 1,
        # we reset lfuCnt to 1.
        self.lfuCnt = 1