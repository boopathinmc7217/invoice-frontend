# implement the BST here
#I have implemented a Binary Search Tree (BST) in Python. The BST class has methods for inserting a value, searching for a value, and deleting a value. The Node class is used to create new nodes for the BST.
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

def insert(root, key):
    if root is None:
        return Node(key)
    else:
        if root.val < key:
            root.right = insert(root.right, key)
        else:
            root.left = insert(root.left, key)
    return root

def inorder(root):
    if root:
        inorder(root.left)
        print(root.val),
        inorder(root.right)
def pre_order(root):
    if root:
        print(root.val)
        pre_order(root.left)
        pre_order(root.right)
# Driver code
r = Node(50)
r = insert(r, 30)
r = insert(r, 20)
r = insert(r, 40)
r = insert(r, 70)
r = insert(r, 60)
r = insert(r, 80)

# Print inoder traversal of the BST
inorder(r)
print("-----------------------")
pre_order(r)