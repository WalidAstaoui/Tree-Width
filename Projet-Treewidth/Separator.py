from Verification import *
from copy import deepcopy
from queue import Queue


def create_s_t_graph(grph, S, T):
    st_g = deepcopy(grph)

    st_g['s'] = set()
    st_g['t'] = set()
    for u in S:
        for v in grph[u]:
            st_g[v].remove(u)
            st_g[v].add('s')
            if v not in S:
                st_g['s'].add(v if v not in T else 't')
    for u in T:
        for v in grph[u]:
            st_g[v].remove(u)
            st_g[v].add('t')
            if v not in T:
                st_g['t'].add(v if v not in S else 's')
    for u in S:
        del st_g[u]
    for u in T:
        del st_g[u]

    lu = list(st_g.keys())
    for u in lu:
        st_g[u + '_'] = set([u])

    for u in lu:
        lgu = list(st_g[u])
        for v in lgu:
            st_g[u].remove(v)
            st_g[u].add(v + '_')
    return st_g




'''print(create_s_t_graph(graph, {'1', '4'}, {'6', '9'}))'''

oo = 1 << 16


def create_residual_graph(st_g):
    res_g = deepcopy(st_g)
    for u in st_g:
        if u[-1] == '_':
            v = u[:-1]
            res_g[u] = {v: 1}
        else:
            res_g[u] = {u + '_': 0}
            for v in st_g[u]:
                res_g[u][v] = oo

    return res_g


'''print(create_residual_graph(create_s_t_graph(graph, {'1', '4'}, {'6', '9'})))'''


def find_size_and_cut_min_vertex_cut(grph, S, T):
    st_g = create_s_t_graph(grph, S, T)
    res_g = create_residual_graph(st_g)

    N = len(res_g)
    size = 0
    cut = set()
    s_area = set()

    while True:
        par = {}
        vis = set()

        q = Queue(maxsize=N)
        q.put('s')
        vis.add('s')

        while not q.empty():
            u = q.get()

            for v in res_g[u]:
                if v not in vis and res_g[u][v] > 0:
                    vis.add(v)
                    q.put(v)
                    par[v] = u
                    
                    if v == 't_':
                        break
            if 't_' in vis:
                break

        if 't_' not in vis:
            for u in res_g:
                if u[-1] != '_' and u not in {'s', 't'}:
                    v = u + '_'
                    if (u in vis) ^ (v in vis):
                        cut.add(u)
                    if u in vis and v in vis:
                        s_area.add(u)
            break

        ds = oo+N
        last = 't_'
        while last in par:
            ds = min(ds, res_g[par[last]][last])
            last = par[last]
        
        size += ds
        last = 't_'
        while last in par:
            res_g[par[last]][last] -= ds
            if par[last] not in res_g[last]:
                res_g[last][par[last]] = 0
            res_g[last][par[last]] += ds
            last = par[last]

    return size, cut, s_area


'''
print(find_size_and_cut_min_vertex_cut(graph, {'1', '4'}, {'6', '9'}))
print(find_size_and_cut_min_vertex_cut(graph, {'7'}, {'3'}))
print(find_size_and_cut_min_vertex_cut(graph, set(), {'3'}))
print([find_size_and_cut_min_vertex_cut(graph, {'1'}, {i}) for i in ['2','3','4','6','7','8','9']])
'''


'''
def verify_min_separator(gr, S, T):
    gph = create_s_t_graph(gr, S, T)
    size, cut = find_size_and_cut_min_vertex_cut(gph)
    sep = set()

    for w in cut:
        vis = set()

        q = ['s']
        vis.add('s')

        while q:
            u = q.pop()
            for v in gph[u]:
                if v not in vis and (v not in cut or v == w):
                    q.append(v)
                    vis.add(v)
                    if v == 't':
                        sep.add(w)
                        break
            if 't' in vis:
                break

        if len(sep) == size:
            break

    if len(sep) != size:
        raise ValueError('Incompatibility Size/Cut')

    return sep
'''


def eliminate_set(grrr, S):
    g = deepcopy(grrr)
    for u in S:
        if u in grrr:
            for v in grrr[u]:
                g[v].remove(u)
    for u in S:
        if u in g:
            del g[u]
    return g


'''print(eliminate_set(graph, {'1', '2', '4'}))'''


def find_all_partitions(W, k):
    partitions = [(set(), set(), set())]
    M = int(2 * len(W) / 3.)
    for u in W:
        nextPartitions = []
        for (AW, SW, BW) in partitions:
            if len(SW) <= k:
                nSW = set(SW)
                nSW.add(u)
                nextPartitions.append((AW, nSW, BW))
            if len(AW) < M:
                nAW = set(AW)
                nAW.add(u)
                nextPartitions.append((nAW, SW, BW))
            if len(BW) < M:
                nBW = set(BW)
                nBW.add(u)
                nextPartitions.append((AW, SW, nBW))
        partitions = nextPartitions

    partitions = [(AW, SW, BW) for (AW, SW, BW) in partitions if len(BW) <= len(AW)]
    partitions.sort(key=lambda x: (-len(x[0]) * len(x[1]) * len(x[2])))
    return partitions


'''print(find_all_partitions({1, 2, 3, 4}, 2))'''


def find_balanced_partition(gr, W, k):
    allPartitions = find_all_partitions(W, k)
    for (AW, SW, BW) in allPartitions:
        grrph = eliminate_set(gr, SW)
        size, cut, s_area = find_size_and_cut_min_vertex_cut(grrph, AW, BW)
        if size + len(SW) >= k + 1:
            continue
        A = AW | s_area
        S = SW | cut
        B = BW

        for u in grrph:
            if u not in A and u not in S:
                B.add(u)

        return True, A, S, B
    return False, [], [], []


'''
def generate_partition(W, k):
    n = len(W)
    lW = list(W)
    M = int(2 * n / 3.)
    bits = [0] * (n + 1)

    for i in range(3 ** n):
        part = [set(), set(), set()]

        for j in range(n):
            xj = (bits[j] + j) % 3
            part[xj].add(lW[j])

        if len(part[0]) <= M and len(part[2]) <= M and len(part[1]) <= k + 1:
            yield part

        bits[0] += 1
        for j in range(n):
            if bits[j] == 3:
                bits[j] = 0
                bits[j + 1] += 1
'''

'''
def find_balanced_partition(gr, W, k):
    generator = generate_partition(W, k)
    n = len(W)
    for i in range(3**n):
        AW, SW, BW = next(generator)
        grrph = eliminate_set(gr, SW)
        size, cut, s_area = find_size_and_cut_min_vertex_cut(grrph, AW, BW)
        if size + len(SW) > k + 1:
            continue
        A = AW | s_area
        S = SW | cut
        B = BW

        for u in grrph:
            if u not in A and u not in S:
                B.add(u)

        return True, A, S, B
    return False, [], [], []
'''


def build_tree_decomposition_with_separator(grr, W, k):
    V = list(grr.keys())
    if W == set(V):
        return Tree(Node(V))
    t, A, S, B = find_balanced_partition(grr, W, k)
    if not t:
        raise ValueError('Tree Width is larger than ' + str(k))

    if (A == set() or B == set()) and S.issubset(W):
        X = set(V) - W
        S.add(next(iter(X)))

    treeA = build_tree_decomposition_with_separator(eliminate_set(grr, (B - S)), S | (W & A), k)
    treeB = build_tree_decomposition_with_separator(eliminate_set(grr, (A - S)), S | (W & B), k)
    root_bag = Node(list(S | W))
    root_bag.add_children([treeA.root, treeB.root])
    return Tree(root_bag)


'''print(build_tree_decomposition_with_separator(graph, set(), 2))'''



'''print(build_tree_decomposition_with_separator(peterson, set(), 3))'''

def min_separator(gr):
    sep = set()
    min_size = oo
    ls = list(gr.keys())
    for i in range(len(gr)):
        if len(gr[ls[i]]) < len(gr) - 1:
            ls[0],ls[i] = ls[i],ls[0]
            break
    else:
        return sep
    i = 0
    while i < min_size:
        u = ls[i]
        for j in range(i+1, len(gr)):
            v = ls[j]
            if v in gr[u]:
                continue
            s, c, _ = find_size_and_cut_min_vertex_cut(gr, {u}, {v})
            if s < min_size:
                min_size = s
                sep = c
        i += 1
    return sep

def is_clique(gr, bag):
    for u in bag:
        for v in bag:
            if u < v and v not in gr[u]:
                return False
    return True

def get_list_of_bags(t):
    L = []
    q = [t.root]
    while q != []:
        bag = q.pop()
        L.append(bag)
        q.extend(bag.children)
    return L

def aux_graph(gr, t, bag):
    aux = {}
    for u in bag:
        aux[u] = set()
    
    bags = t[bag]
    for b in bags:
        bb = b & bag
        for u in bb:
            for v in bb:
                if u != v:
                    aux[u].add(v)
    
    for u in bag:
        for v in bag:
            if v in gr[u]:
                aux[u].add(v) 
    
    return aux

def refine(gr, t):
    bag_x = frozenset()
    for bag in t:
        if len(bag) > len(bag_x) and not is_clique(gr, bag):
            bag_x = bag
    
    if len(bag_x) == 0:
        print("Can t refine, all bags are cliques")
        return False
    
    H = aux_graph(gr, t, bag_x)
    S = frozenset(min_separator(H))
    
    if len(S) == 0:
        print("Can t refine more, aux graph is clique")
        return False
    
    H_S = eliminate_set(H, S)
    W = []
    
    vis = set()
    
    for u in H_S:
        if u in vis: continue
        vis.add(u)
        Q = [u]
        w = set()
        
        while Q != []:
            x = Q.pop()
            w.add(x)
            for v in H_S[x]:
                if v in vis: continue
                vis.add(v)
                Q.append(v)
        
        W.append(frozenset(w))
    
    T_bags = [S | w for w in W]
    for t_bag in T_bags:
        t[t_bag] = set()
            
    adj_x = list(t[bag_x])
    
    for bag in adj_x:
        t[bag_x].remove(bag)
        t[bag].remove(bag_x)
    
    for bag in adj_x:    
        for i in range(len(T_bags)):
            if (bag & bag_x).issubset(T_bags[i]):
                t[T_bags[i]].add(bag)
                t[bag].add(T_bags[i])              
                break   
            
    del t[bag_x]       
    t[S] = set()
    
    for i in range(len(T_bags)): 
        t[S].add(T_bags[i])
        t[T_bags[i]].add(S)
        
    return True

def tree_from_t(t):
    root_bag = next(iter(t))
    root_node = Node(list(root_bag))
    
    vis = set()
    vis.add(root_bag)
    Q = [(root_bag, root_node)]
    
    while Q != []:
        bag, bag_node = Q.pop()
        for v_bag in t[bag]:
            if v_bag in vis: continue
            vis.add(v_bag)
            v_node = Node(list(v_bag))
            v_node.add_parent(bag_node)
            Q.append((v_bag, v_node))
    
    return Tree(root_node)

def initial_t(gr):
    return {frozenset(gr.keys()) : set()}

def build_tree_decomposition_from_refining(gr):
    t = initial_t(gr)
    print(tree_from_t(t), end = '')
    while(refine(gr, t)):
        print(tree_from_t(t), end = '')
        
              
graph_1 = {'1': {'2', '4'}, '2': {'1', '5'}, '4': {'1', '5'}, '5': {'2', '4', '6', '9'}, '6': {'5', '9'},
           '9': {'5', '6'}}

print(min_separator(graph_1))
build_tree_decomposition_from_refining(graph_1)

graph_2 = {}
graph_2['1'] = {'4', '2'}
graph_2['2'] = {'1', '3', '8'}
graph_2['3'] = {'2', '6'}
graph_2['4'] = {'7', '1'}
graph_2['6'] = {'9', '3'}
graph_2['7'] = {'4', '8'}
graph_2['8'] = {'7', '9', '2'}
graph_2['9'] = {'8', '6'}

print(min_separator(graph_2))
build_tree_decomposition_from_refining(graph_2)

graph_3 = {'5': {'2', '4', '6', '8'}, '2': {'5'}, '4': {'5', '1', '0'}, '1': {'4', '0'}, '0': {'4', '1'}, '6': {'5', 'a', 'c'},
           'a': {'6', 'b'}, 'b': {'a', 'c'}, 'c': {'b', '6'}, '8': {'5', '7', '9'},'7': {'8'},'9': {'8'}}

print(min_separator(graph_3))
build_tree_decomposition_from_refining(graph_3)

peterson = {}
peterson['0'] = {'1', '5', '6'}
peterson['1'] = {'0', '2', '7'}
peterson['2'] = {'1', '3', '8'}
peterson['3'] = {'2', '4', '9'}
peterson['4'] = {'3', '5', 'A'}
peterson['5'] = {'0', '4', 'B'}
peterson['6'] = {'0', '8', 'A'}
peterson['7'] = {'1', '9', 'B'}
peterson['8'] = {'2', '6', 'A'}
peterson['9'] = {'3', '7', 'B'}
peterson['A'] = {'4', '6', '8'}
peterson['B'] = {'5', '7', '9'}

print(min_separator(peterson))
build_tree_decomposition_from_refining(peterson)
