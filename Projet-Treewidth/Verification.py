from Classes import Tree, Node
from Path_decomposition import set_substraction
from Tree_decomposition import canonical_tree
from collections import defaultdict

# hash pour être rigoureux

def fill_dict(tree):
    ''' Gives all the (possible) edges and vertices 
    that the original graph can have, given that (tree) is its tree decomposition.
    Parameters:
        tree (Tree object)
    Returns:
        adj_list (defaultdict)'''

    adj_list=defaultdict(lambda: [])
    def bfs(node):
        ''' Using BFS to fills the dict adj_list with 
            the vertices and edges encountered starting from node.
        Parameters:
            node (Node object)'''

        for i in node.value:
            if i not in adj_list:
                adj_list[i]=[]
            for j in node.value:
                if i!=j and j not in adj_list[i]:
                    adj_list[i].append(j)
                    adj_list[j].append(i)
        for child in node.children:
            bfs(child)

    bfs(tree.root)
    return adj_list


def check_vertices_edges(tree,graph):
    ''' Checks whether the tree contains every vertex and every edge of the initial graph.
    Parameters:
        tree (Tree object)
        graph (defaultdict)
    Returns:
        boolean'''
    
    adj_list=fill_dict(tree)
    for vertex in graph.keys():
        if vertex not in adj_list:
            return False
    for vertex_1 in graph.keys():
        for vertex_2 in graph[vertex_1]:
            if vertex_2 not in adj_list[vertex_1]:
                return False
    return True


def is_connected(tree, graph):
    ''' Checks if, for every vertex (v) of the graph, the subgraph induced by the nodes containing (v) is connected,
        by comparing the size of some subtree where all nodes contain (v) 
        and the number of occurences of (v) in the whole tree.
    Parameters:
        tree (Tree object)
        graph (defaultdict)
    Returns:
        boolean '''

    def find_first(node,index):
        ''' Using DFS, finds the first node containing a vertex.
        Parameters:
            node (Node object)
            index (str)
        Returns:
            Node object or None'''

        if index in node.value:
            return node
        for child in node.children:
            if find_first(child,index) is not None:
                return find_first(child,index)
        return None

    def size_connected_subtree(node,index):
        ''' Using DFS and starting from (node) given by find_first, 
            computes the size of the subtree where each node contains (index).
        Parameters:
            node (Node object)
            index (str)
        Returns:
            size (int)'''

        size=0
        if index in node.value:
            size+=1
            for child in node.children:
                size+=size_connected_subtree(child,index)
            return size
        else:
            return 0

    def count_occurences(node,vertex):
        ''' Using DFS, counts the number of occurences of vertex starting from node.
        Parameters:
            node (Node object)
            vertex (str)
        Returns:
            occurences (int)'''

        occurence=0
        if vertex in node.value:
            occurence+=1
        for child in node.children:
            occurence+=count_occurences(child,vertex)
        return occurence

    def aux(tree,vertex):
        ''' For a given vertex, 
            checks if the subgraph induced by the nodes containing index is connected.
        Parameters:
            tree (Tree object)
            vertex (int)
        Returns:
            boolean'''
        
        count_total=count_occurences(tree.root,vertex)

        count_subtree=size_connected_subtree( find_first(tree.root,vertex), vertex)

        return count_total==count_subtree
    
    for vertex in graph.keys():
        if not aux(tree,vertex):
            return False

    return True


def is_tree_decomposition(tree,graph):
    ''' Checks if tree is a tree decomposition of graph.
    Parameters: 
        tree (Tree object)
        graph (defaultdict)
    Returns:
        boolean'''

    if not is_connected(tree,graph) or not check_vertices_edges(tree,graph):
        return False
    return True

def is_nice_tree(tree):
    ''' Using DFS, checks if tree (supposedly a tree decomposition)
        satisfies the conditions of nice tree decomposition.
    Parameters:
        tree (Tree object)
    Returns:
        boolean'''

    # à changer: la racine est vide ? si les feuilles sont vides ? + fausse

    def aux(node):
        if len(node.children)>2:
            return False
        elif len(node.children)==2 and not (set(node.value)==set(node.children[0].value)==set(node.children[1].value) ):
            print(node)
            return False
        elif len(node.children)==1:
            child=node.children[0]
            # the condition belows is to test 
            # if node included in child or the inverse, 
            # which should be the case in nice tree decomp
            if len(set_substraction(node,child))+len(set_substraction(child,node))>1:
                return False
        for child in node.children:
            if not aux(child):
                return False
        return True
    
    return aux(tree.root)


def generate_degree_bounded_graph(N, d):
    gr = {}
    for i in range(N):
        gr[str(i)] = set()
        if i:
            gr[str(i)].add(str(i-1))
            gr[str(i-1)].add(str(i))
    
    for i in range(N):
        d_i = random.randint(1,d)
        ls_j = list(range(N))
        random.shuffle(ls_j)
        for j in ls_j:
            if j == i: continue
            if len(gr[str(i)]) >= d_i:
                break
            if len(gr[str(j)]) == d:
                continue
            gr[str(i)].add(str(j))
            gr[str(j)].add(str(i))
            
    return gr

print(generate_degree_bounded_graph(10, 4))