class Node:
    def __init__(self, key, value):
        self.key = key
        self.val = value
        self.next = None
        self.prev = None

class LRUCache:
    """
    MENTAL MODEL

    We maintain a Doubly Linked List like this:

        head <-> ... <-> ... <-> tail

    Where:
        - head is a DUMMY node
        - tail is a DUMMY node

    REAL nodes are always between head and tail.

    FRONT vs END:
    -------------------------------------------

        FRONT (head.next):
            => Least Recently Used (LRU)
            => This is what we REMOVE when capacity exceeds

        END (tail.prev):
            => Most Recently Used (MRU)
            => This is where we INSERT / MOVE nodes

    OPERATIONS:
    -------------------------------------------

        get(key):
            - fetch node from hashmap
            - move it to END (because it is now recently used)

        put(key, value):
            - if key exists:
                remove old node
            - insert new node at END (MRU)
            - if over capacity:
                remove node from FRONT (LRU)

    NOTE: V. Important
    WHY SENTINEL NODES?
    -------------------------------------------

        head and tail are NEVER None

        So:
            - no special edge-case checks
            - no "if list empty" logic everywhere

    DATA STRUCTURES:
    -------------------------------------------

        hashmap: key -> node      => O(1) lookup
        DLL: maintains order      => O(1) insert/remove

    """

    def __init__(self, capacity):
        self.capacity = capacity
        # hashmap for O(1) access => key -> node
        self.cache = {}
        # create dummy head and tail
        self.head = Node(-1, -1)
        self.tail = Node(-1, -1)

        # connect dummy nodes
        self.head.next = self.tail
        self.tail.prev = self.head

    def insert(self, new_node):
        """
        Insert node at the END (right before tail).

        END = Most Recently Used (MRU)
        """
        # we get the current node at the end which is tail.prev
        # since we are using dummy nodes for tail and head
        # so:
        tail_end = self.tail.prev
        # then we will insert the new node after the tail end:
        tail_end.next = new_node
        # rewire the new node's pointers now:
        new_node.prev = tail_end
        new_node.next = self.tail
        # and the tail dummy node should also point to the new node now:
        self.tail.prev = new_node

    def remove(self, node):
        """
        Remove a node from the DLL in O(1).

        Works because we already have direct reference
        to the node (via hashmap).
        """
        # we need to update the node's pointers and its next and previous
        # node;s pointers:
        next_node = node.next
        prev_node = node.prev
        
        # the node next to it's previous should 
        # point to the node previous to the one we are removing:
        next_node.prev = prev_node
        # the node previous to it should point to the node next 
        # to the one we are removing:
        prev_node.next = next_node
        
        # let the current one's pointers be pointing to None:
        node.next = node.prev = None

    def get(self, key):
        """
        If key exists:
            - move it to END (MRU)
            - return value

        If not:
            - return -1
        """
        # if the key does not exist in the cache:
        if key not in self.cache:
            return -1

        # if it exists, fetch it:
        # remember: we are saving the node itself in the map:
        # so we are fetching the node itself!
        node = self.cache[key]

        # remove it - wherever it is:
        self.remove(node)
        # and then insert it - we are inserting at the end
        # move to END (MRU)
        self.insert(node)

        # and return the value:
        return node.val

    def put(self, key, value):
        """
        Insert or update key.

        Always:
            - node ends up at END (MRU)

        If capacity exceeded:
            - remove from FRONT (LRU = head.next)
        """
        # first check if the key already exists in the cache:
        if key in self.cache:
            # if it does, get the associated node, and
            # remove it:
            node = self.cache[key]
            self.remove(node)

        # otherwise, we create the node, and add it to the map:
        new_node = Node(key, value)
        self.cache[key] = new_node
        # and also insert it into our list:
        # remember: insert at END (MRU)
        self.insert(new_node)

        # and if we exceeded our capacity, simply remove the node from our head (FRONT):
        if len(self.cache) > self.capacity:
            # use next as head uses a sentinel/dummy node
            node_to_remove = self.head.next
            self.remove(node_to_remove)
            
            # and remove it from our hashmap as well
            del self.cache[node_to_remove.key]
        

# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)