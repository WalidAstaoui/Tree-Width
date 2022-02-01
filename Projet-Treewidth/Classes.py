import networkx as nx
import matplotlib.pyplot as plt

from sidefunctions import hierarchy_pos
from sidefunctions import even_hierarchy_pos

class Node:
    ''' A class used to represent a node of a tree

    Attributes
    ----------
    value : str
    parent : a Node object
    children : a list of Node objects

    Methods
    -------
    add_children :  adds a list of children to the node
    add_parent : adds a parent to the node
    delete_edge : deletes the edge between the node and another
    ___str___: gives a basic visual representation of the node, together with its parent and children'''

    def __init__(self, value=[]):
        ''' Initializes the Node object with the value given in parameters, otherwise it's just an empty Node.
        Parameters:
            value (str list)'''

        self.value = value
        self.parent = None
        self.children = []

    def add_children(self, list_children):
        ''' Adds a list of Node objects to the already existing self.children, and adds self as a parent to these nodes.
        Parameters: 
            list_children (Node objects list)'''

        self.children.extend(list_children)
        for child in list_children:
            child.parent = self

    def add_parent(self, node):
        ''' Makes a node a parent to self, and adds self as a child to the list of children to the parent
        Parameters:
            node (Node object)'''

        self.parent = node
        (node.children).append(self)

    def delete_edge(self, node):
        ''' Deletes the edge between self and node (if it exists). 
        Parameters:
            node (Node object)'''
        if node == self.parent:
            self.parent = None
            node.children.remove(self)
        elif node in self.children:
            self.children.remove(node)
            node.parent = None

    def __str__(self):
        ''' gives a visual representation of the node, its parent and its children'''

        string = ''
        if self.parent is not None:
            string += "("+",".join(self.parent.value)+")"+'\n|\n'
        string += "("+",".join(self.value)+")"+'\n|\n'
        for child in self.children:
            string += "("+",".join(child.value)+")"+' '
        return string


class Tree:
    ''' A class used to represent a tree, by knowing only its root

    Attributes
    ----------
        root (Node object)

    Methods
    -------
        width : gives the width of the tree
        size : gives the size of the tree
        ___str___ : gives a very basic and ugly representation of the tree'''

    def __init__(self, root):
        ''' Initializes the Tree object given its root.
        Parameters:
            root (Node object)'''

        self.root = root

    def width(self):
        ''' Gives the width of the tree.
        Returns:
            width (int)'''

        def bfs(level):
            ''' aux function that uses BFS to computes the largest width on a level and calls itself on the next one
            Parameters: 
                level (Node objects list)
            Returns:
                max_cardinal_sub_graph (int): the maximum cardinal of all the nodes in the subgraph starting from level'''

            if any(level):
                next = []
                result = 0
                for node in level:
                    result = max(result, len(node.value))
                    next.extend(node.children)
                return max(result, bfs(next))
            else:
                return 0
        
        return bfs([self.root])-1  # reminder: width=cardinal of a X -1

    def size(self):
        ''' Gives the size of the tree
        Returns:
            size (int)'''
    
        def bfs(level):
            '''aux function that use BFS to computes the number of nodes on a level, and calls itself on the next one.
            Parameters:
                level (Node object list)
            Returns:
                size_subgraph (int): size of the subgraph starting from level'''

            if any(level):
                next = []
                result = 0
                for node in level:
                    result += 1
                    next.extend(node.children)
                return result+bfs(next)
            else:
                return 0
    
        return bfs([self.root])


    def __str__2(self):
        '''gives an ugly vizualization of the tree, example:
        0|
        1-2|
        3|4-5|
        means nodes 1 and 2 are both children of 0, 3 is the child of 1
        and 4 and 5 are children of 2
        
        Returns:
            representation (str)'''
        
        def represent(list_of_lists):
            '''aux function that use BFS to print all nodes on a level and calls itself on the next one.
            Parameters:
                list_of_lists ( (Node objects list) list) 
            Returns:
                sub_representation (str)'''

            if any(list_of_lists):  # if the level is not empty
                next = []
                result = ''
                for group in list_of_lists:  # a group is a list of children of a specific node
                    if any(group):  # to check if there is any children left
                        level = []
                        for node in group:
                            if len(node.value) != 0:
                                level.append( "("+",".join(node.value)+")" )
                            else:
                                level.append("Ø")
                            next += [node.children]
                        # children of the same node are separated by '-'
                        result += "-".join(level)
                    result += "|"  # separates children of two differents nodes
                result += "\n"
                # to go from the actual level to the next one
                return result+represent(next)

            else:  # checks if the level is empty to end recursion
                return ''

        return represent([[self.root]])
    
    def brute_force(self):
        ''' Enforces that every child of a node in the tree satisfy node==child.parent.'''
        def DFS(node):
            for child in node.children:
                child.parent=node
                DFS(child)
        DFS(self.root)
    
    def __str__(self):
        ''' Using matplotlib and networkx, output a vizual representation of the tree, 
        and prints an empty string in the console.
        
        Returns:
            empty str'''

        self.brute_force()
        graph=nx.Graph()
        correspondance=[]
        graph.nodes(data=True)
        d={}
        def DFS(node):
            if correspondance==[]:
                graph.add_node(0)
                correspondance.append(node)
                if node.value==[]:
                    d[0]="Ø"
                else:
                    d[0]=",".join(node.value)

                for child in node.children:
                    #the problem starts here, because child.parent =/= node (equality of memory adresses)
                    DFS(child)
            else:
                index_node=len(correspondance)
                graph.add_node( index_node )
                if node.value==[]:
                    d[index_node]="Ø"
                else:
                    d[index_node]=",".join(node.value)
                correspondance.append(node)
                index_father=correspondance.index(node.parent)
                graph.add_edge(index_father,index_node)
                for child in node.children:
                    DFS(child)
        
        DFS(self.root)
        pos = nx.spring_layout(graph)
        nx.draw(graph,pos,labels=d,with_labels=True,node_size=[100+100*len(node) for node in d.values()],node_color=['red' if u != 0 else 'orange' for u in d]
                ,font_size = 6)
        plt.show()
        return ""