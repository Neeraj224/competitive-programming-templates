class TreeNode:
    def __init__(self, val = 0, left = None, right = None):
        self.val = val
        self.left = left
        self.right = None

###################################### CREATING TREES FROM THE ELEMENTS OF AN ARRAY: ###################################### 

def buildTreeRecursive(arr, i, n):
    """
        # arr is the list we will build with; i is the current
        # index we're at in the array.
        # n is the total length of the array
    """
    root = None
    
    if i < n and arr[i] is not None:
        # for the ith position in the array
        root = TreeNode(arr[i])
        # its left child will be at the (2*i + 1) position
        root.left = buildTreeRecursive(arr, (2 * i) + 1, n)
        # and its right child will be at the (2*i + 2) position
        root.right = buildTreeRecursive(arr, (2 * i) + 2, n)
    
    return root

def buildTreeIterative(arr):
    # obviously if the array is empty:
    if len(arr) == 0:
        # return Nothing
        return None
    
    # this is the queue that will store the nodes temporarily
    nodes = []
    # we take the first element of the array
    val = arr.pop(0)
    # and make it the root node
    root = TreeNode(val)
    nodes.append(root)
    
    # while there are elements in the array:
    while len(arr) > 0:
        curr = nodes.pop(0)
        
        left_val = arr.pop(0)
        
        if left_val is not None:
            curr.left = TreeNode(left_val)
            nodes.append(curr.left)
            
        if len(arr) > 0:
            right_val = arr.pop(0)
            
            if right_val is not None:
                curr.right = TreeNode(right_val)
                nodes.append(curr.right)
    
    return root

###################################### TREE TRAVERSALS: ###################################### 

def levelOrder(root):
    """
        this is the normal level-order:
        the level order traversal will be received in just an array:
    """
    traversal = []
    
    if root is None:
        return traversal
    
    queue = []
    # push the root first
    queue.append(root)
    
    while len(queue) > 0:
        current = queue[0]
        # if theres a left child:
        if current.left:
            # append it to the queue
            queue.append(current.left)
        # if there is a right child:
        if current.right:
            # append it to the queue:
            queue.append(current.right)
        
        traversal.append(queue.pop(0).val)
        
    return traversal

def levelOrderLeet(root):
    """
        levelOrderLeet() does level orders the leetcode-way:
        -> every level is appended as a subarray for the tree's
        level order!
    """
    traversal = []
    
    if root is None:
        return traversal
    
    queue = []
    # push the root first
    queue.append(root)
    
    while len(queue) > 0:
        level = []
        
        for _ in range(len(queue)):
            current = queue[0]
            # if theres a left child:
            if current.left:
                # append it to the queue
                queue.append(current.left)
            # if there is a right child:
            if current.right:
                # append it to the queue:
                queue.append(current.right)
            
            level.append(queue.pop(0).val)
        
        traversal.append(level)
        
    return traversal

def inorder(root):
    if not root:
        return
    
    inorder(root.left)
    print(root.val, end = " ")
    inorder(root.right)

def preorder(root):
    if not root:
        return
    
    print(root.val, end = " ")
    preorder(root.left)
    preorder(root.right)

def postorder(root):
    if not root:
        return
    
    postorder(root.left)
    postorder(root.right)
    print(root.val, end = " ")
    
###################################### Popular algorithms: ###################################### 

def maxDepth(root):
    def dfs(root, depth):
        if not root:
            return depth
        
        return max(dfs(root.left, depth + 1), dfs(root.right, depth + 1))
    
    return dfs(root, 0)

###################################### DRIVER CODE: ###################################### 

def main():
    arr1 = [i for i in range(10)]
    arr2 = [3, 9, 20, None, None, 15, 7]
    
    tree1 = buildTreeRecursive(arr1, 0, len(arr1))
    tree2 = buildTreeRecursive(arr2, 0, len(arr2))
    
    print("inorder traversal: ", end = "")    
    inorder(tree1)
    print("")
    
    print("preorder traversal: ", end = "")    
    preorder(tree1)
    print("")
    
    print("postorder traversal: ", end = "")    
    postorder(tree1)
    print("")
    
    print("level order traversal:")
    print(levelOrder(tree1))
    print(levelOrder(tree2))
    
    print("level order traversal - the LEET way!")
    print(levelOrderLeet(tree1))
    print(levelOrderLeet(tree2))
    
    
if __name__ == "__main__":
    main()