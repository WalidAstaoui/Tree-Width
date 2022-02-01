from Classes import Node, Tree

def set_substraction(node1,node2):
    ''' Returns the set node1 - node 2 in the form of a list
    Parameters:
        node1 (Node object)
        node2 (Node object)
    Returns:
        set_minus (str list)'''

    set_minus=[]
    for element in node1.value:
        if element not in node2.value:
            set_minus.append(element)
    return set_minus

def canonical_path(parent,child): 
    ''' Transforms the path between a parent and its child into a canonical one.
    Parameters:
        path is non needed, changes are to be made
        parent (Node object)
        child (Node object)'''
        
    starting_set_minus=set_substraction(parent,child) 
    #list of char that we should get rid of as they don't appear in child.value
    arrival_set_minus=set_substraction(child,parent)
    #list of char that we should add to reach the child
    parent.delete_edge(child)
    #we substitude this edge by the new nodes
    
    temp_value=parent.value[:]
    former_node=parent

    #first step: adding forget nodes until reaching the node with value (node1.value intersect node2.value)
    for element in starting_set_minus:
        temp_value.remove(element)#waaaaaaaaaaas here
        actual_node=Node(temp_value[:])
        actual_node.add_parent(former_node)
        former_node=actual_node
    
    #second step: add nodes
    if len(arrival_set_minus)==0:
        #if node2.value included in node1.value then the former_node.value=node2.value
        #so no need to have the two in the path
        former_node.add_children(child.children)
        #beware, the child is no longer part of the path

    if len(arrival_set_minus)>=1: 
        # because the arrival node aka node2 is already in the tree/path:
        # no need to add a node that has the same value
        arrival_set_minus=arrival_set_minus[:-1]
    
        #second step: add nodes until reaching the node2
        for element in arrival_set_minus:
            temp_value.append(element)
            actual_node=Node(temp_value[:])
            actual_node.add_parent(former_node)
            former_node=actual_node
        
        child.add_parent(former_node)

    

def nice_path(path):
    ''' Transforms a path (a particular case of Tree object) into a nice one.
    Parameters:
        path (Tree object)'''

    if path.root.value!="": 
        #in case the root is non empty, we add an empty node as a root
        empty_node=Node()
        path.root.add_parent(empty_node)
        path.root=empty_node
    
    actual_node=path.root
    while actual_node.children!=[]:
        former_node=actual_node
        actual_node=former_node.children[0] #there is only a child each time
        canonical_path(former_node,actual_node)
    if actual_node.value!="":
        #in case the last node of the path is non empty, we add an empty node at the end
        former_node=actual_node
        empty_node=Node('')
        empty_node.add_parent(former_node)
        canonical_path(former_node,empty_node)