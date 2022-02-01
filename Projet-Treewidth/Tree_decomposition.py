from Classes import Node, Tree
from Path_decomposition import canonical_path


def join_subtree(parent, children,flag):
    ''' Makes the tree satisfy the condition:
        a node cannot have more than two children, 
        and if that's the case they should have the same value as their father.
    Parameters:
        parent (Node object)
        children (Node object list)
        flag (boolean)'''

    #flag is here just for us to know if we still need to remove the edges between the "original" children and their parent
    children=children[:]    #won't work with deepcopy
    if not flag:
        flag=True
        for child in children:
            parent.delete_edge(child)
    if len(children)==1:
        parent.add_children(children)
    else:
        #left subtree: 
        # if the child is different from the parent,
        # we add a node of value parent.value between parent and child
        # else, we just (re)connect the child and the parent
        if set(children[0].value)!=set(parent.value):
            parent_left=Node(parent.value)
            parent_left.add_parent(parent)
            children[0].add_parent(parent_left)
        else:
            children[0].add_parent(parent)
            
        #right subtree:
        #we start by adding the right child of the parent with the value parent.value
        parent_right=Node(parent.value)
        parent_right.add_parent(parent)
        #apply join_subtree on the parent_right and the remaining children
        join_subtree(parent_right,children[1:],flag)

def adding_join_subtree(parent, children):
    ''' Applies join_subtree between every non-leaf node and its children.
        (when a node has only a child, join_subtree don't change anything) 
    Parameters: 
        parent (Node object)
        children (Node object list)'''
    
    if any(children):
        next=[]
        for child in children:
            next.append((child,child.children))
        join_subtree(parent,children,False)
        for (a,b) in next:
            adding_join_subtree(a,b)

def adding_empty_leaves(tree):
    ''' Adds empty leaves to the tree if needed, 
        and if the root is non empty, adds an empty root.
    Parameters:
        tree (Tree object) '''

    def aux(node):
        ''' Using BFS to reach all the leaves of tree, and adds empty node as a child to it if needed.
        Parameters:
            node (Node object)'''

        if node.children!=[]:
            for child in node.children:
                aux(child)
        else:
            if node.value!=[]:
                empty_node=Node()
                empty_node.add_parent(node)

    if tree.root.value!=[]:
        empty_node=Node()
        tree.root.add_parent(empty_node)
        tree.root=empty_node
    aux(tree.root)


def adding_canonical_paths(parent,children):
    ''' Using BFS to make the path between a parent and its children a canonical path.
    Parameters:
        parent (Node object)
        children (Node object list)'''
        
    if len(children)>1:
        #since in the function canonical_tree, we apply apply_join_subtree before this function, 
        #we know that whenever a node has multiple children, they are all the same.
        for child in children:
            adding_canonical_paths(child,child.children)
    elif len(children)==1:
        child=children[0]
        canonical_path(parent,child)
        adding_canonical_paths(child,child.children)

def canonical_tree(tree):
    ''' Transforms any tree decomposition into a nice one.
    Parameters:
        tree (Tree object)'''
    adding_join_subtree(tree.root,tree.root.children)
    adding_empty_leaves(tree)
    adding_canonical_paths(tree.root,tree.root.children)