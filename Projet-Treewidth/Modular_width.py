from Verification import *
from copy import deepcopy
from queue import Queue

graph_2 = {'1': {'2', '4'}, '2': {'1', '5'}, '4': {'1', '5'}, '5': {'2', '4', '6', '9'}, '6': {'5', '9'}, '9': {'5', '6'}}

def complement(graph):
    cpl_graph = {}
    for u in graph:
        cpl_graph[u] = set()
        for v in graph:
            if v != u and not (v in graph[u]):
                cpl_graph[u].add(v)
    return cpl_graph

print(complement(graph_2))

def sub_graph(graph, S):
    sub_g = {}
    for u in S:
        sub_g[u] = graph[u] & S
    return sub_g

print(sub_graph(graph_2, {'1', '5', '9'}))

def components(graph):
    comps = []
    N = len(graph)
    
    q = Queue(maxsize=N)
    vis = set()
    
    for x in graph:
        if x in vis:
            continue
        
        comp = set()
        q.put(x)
        vis.add(x)
    
        while not q.empty():
            u = q.get()
            comp.add(u)
    
            for v in graph[u]:
                if v in vis:
                    continue
                q.put(v)
                vis.add(v)
    
        comps.append(comp)
    
    return comps

print(components(sub_graph(graph_2, {'1','2','4','6','9'})))

def splitters(graph, m):
    s = set()
    if len(m) == 1:
        return s
    ext_adj = set()
    for u in m:
        ext_adj = ext_adj | (graph[u] - m)
    for u in m:
        s = s | (ext_adj - (graph[u] - m))
    return s

print(splitters(graph_2, {'2','4'}))
print(splitters(graph_2, {'1','2','4'}))
print(splitters(graph_2, {'1','2'}))
print(splitters(graph_2, {'4', '6', '9'}))

def test_add(graph, m, u):
    future_m = set(m)
    
    spl = {u}
    while len(spl):
        future_m = future_m | spl
        spl = splitters(graph, future_m)
    
    return len(future_m) < len(graph) 

print(test_add(graph_2, set(), '1'))
print(test_add(graph_2, {'1'}, '2'))
print(test_add(graph_2, {'2'}, '4'))
print(test_add(graph_2, {'2'}, '1'))

def modular_decomposition(graph):

    nodes = frozenset(graph.keys())
    decomposition = {nodes : []}
    modular_width = 1
    
    if len(nodes) == 1:
        return modular_width, decomposition
    
    comps = components(graph)
    if len(comps) > 1:   
        for comp in comps:
            decomposition[nodes].append(comp)
            w, decomp = modular_decomposition(sub_graph(graph, comp))
            modular_width = max(modular_width, w)
            decomposition.update(decomp)
        return modular_width, decomposition
    
    comps = components(complement(graph))
    if len(comps) > 1:
        for comp in comps:
            decomposition[nodes].append(comp)
            decomp = modular_decomposition(sub_graph(graph, comp))[1]
            modular_width = max(modular_width, len(comp))
            decomposition.update(decomp)
        for comp_1 in comps:
            for comp_2 in comps:
                if comp_1 != comp_2:
                    u = next(iter(comp_1))
                    for v in graph[u]:
                        if v in comp_2:
                            decomposition[frozenset(comp_1)].append(comp_2)
                            break
        return modular_width, decomposition
    
    picked = set()
    modules = []
    for u in graph:
        if u in picked:
            continue
        module = {u}
        picked.add(u)
        
        for v in graph:
            if v in picked:
                continue
            if test_add(graph, module, v):
                module.add(v)
                picked.add(v)
                
        modules.append(module)
    
    for module in modules:
        decomposition[nodes].append(module)
        decomp = modular_decomposition(sub_graph(graph, module))[1]
        modular_width = max(modular_width, len(module))
        decomposition.update(decomp)
        
    for module_1 in modules:
            for module_2 in modules:
                if module_1 != module_2:
                    u = next(iter(module_1))
                    for v in graph[u]:
                        if v in module_2:
                            decomposition[frozenset(module_1)].append(module_2)
                            break
                        
    return modular_width, decomposition    
    
print(modular_decomposition(graph_2))
    
graph_5 = {}
graph_5['1'] = {'2','3','4'}
graph_5['2'] = {'1','4','5','6','7'}
graph_5['3'] = {'1','4','5','6','7'}
graph_5['4'] = {'1','2','3','5','6','7'}
graph_5['5'] = {'2','3','4','6','7'}
graph_5['6'] = {'2','3','4','5','8','9','A','B'}
graph_5['7'] = {'2','3','4','5','8','9','A','B'}
graph_5['8'] = {'6','7','9','A','B'}
graph_5['9'] = {'6','7','8','A','B'}
graph_5['A'] = {'6','7','9','B'}
graph_5['B'] = {'6','7','9','A'}

print(modular_decomposition(graph_5))

        
                
    