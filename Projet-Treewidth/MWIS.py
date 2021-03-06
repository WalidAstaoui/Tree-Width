from Verification import *

'''
def subsets(l):
    if l == []:
        return [[]]
    r = subsets(l[:-1])
    return r + [e + [l[-1]] for e in r]
print(subsets([1,2,3]))
'''


def is_indep(S, graph): #vérifique qu'un sous ensemble est indépendant
    for s in S:
        for e in graph[s]:
            if e in S:
                return False
    return True


tree = Tree(Node(['1', '2']))


def max_w_indep_set(tree, graph):
    canonical_tree(tree)
    print(tree)
    # on va stocker les valeurs de c[t,S] dans un dictionnaire D et l'independant set  dans un dictionnaire S (on utilise une liste pour stocker ce set)
    def compute(u):
        if not u.children:   #si u est une feuille donc l'ensemble vide
            return {frozenset(): 0},{frozenset():[]}

        Du = {}
        Su = {}
        if len(u.children) == 2: #c'est le cas où u est un join node (ie il a deux fils)
            v1, v2 = u.children
            D1 = compute(v1)[0]
            D2 = compute(v2)[0]
            S1 = compute(v1)[1]
            S2 = compute(v2)[1]
            for s in D1:
                Du[s] = D1[s] + D2[s] - sum([int(e) for e in s])  #on applique la formule d'induction
                Su[s] = S1[s] + S2[s]  #l'independant set  associé à u est l'union des deux independant set  associer à v1 et v2
            return Du,Su

        v = u.children[0]
        Dv = compute(v)[0]
        Sv = compute(v)[1]

        if len(u.value) < len(v.value): #si u est un forget node
            x = str(set_substraction(v, u)[0])
            for s in Dv:
                if not x in s:
                    sx = s | frozenset([x])
                    Du[s] = max(Dv[s], Dv[sx]) # on applique la formule d'induction, en fonction du cas on associe à u l'independant set de s dans le sous arbre ayant v pour racine ou celui de sx dans l'arbre ayant v pour racine
                    if Dv[sx] >Dv[s]:
                        Su[s] = Sv[sx]
                    else:
                        Su[s] = Sv[s]
                    
            return Du,Su
        #si u est un introduce nodce
        x = str(set_substraction(u, v)[0])
        for s in Dv:
            Du[s] = Dv[s]
            Su[s] = Sv[s] #comme u est un introduce node, s ne contient pas x et on applique la formule d'induction
            sx = s | frozenset([x])
            Du[sx] = (Dv[s] + int(x) if is_indep(sx, graph) else float('-inf')) #on calcule ici les valeurs de C[t, sx], sx contient x par définition de sx
            Su[sx] = Sv[s] + [x]
        return Du,Su

    return compute(tree.root)


graph = {}
graph['0'] = {'9', '2', '3'}
graph['9'] = {'0', '6', '7'}
graph['6'] = {'9'}
graph['7'] = {'9'}
graph['2'] = {'0', '8'}
graph['8'] = {'2'}
graph['3'] = {'0', '4', '5'}
graph['4'] = {'3', '5'}
graph['5'] = {'3', '4'}

a0 = Node(['0'])

a03 = Node(['0', '3'])
a03.add_parent(a0)

a345 = Node(['3', '4', '5'])
a345.add_parent(a03)

a02 = Node(['0', '2'])
a02.add_parent(a0)

a28 = Node(['2', '8'])
a28.add_parent(a02)

a09 = Node(['0', '9'])
a09.add_parent(a0)

a967 = Node(['9', '6', '7'])
a967.add_parent(a09)

tree = Tree(a0)

print(max_w_indep_set(tree, graph))

graph = {}
graph['7'] = {'4', '8'}
graph['8'] = {'7', '4', '6', '9', '2'}
graph['9'] = {'8', '6'}
graph['4'] = {'7', '8', '1', '2'}
graph['6'] = {'8', '9', '2', '3'}
graph['1'] = {'4', '2'}
graph['2'] = {'1', '4', '3', '6', '8'}
graph['3'] = {'2', '4'}

a248 = Node(['2','4','8'])
a268 = Node(['2','6','8'])
a124 = Node(['1','2','4'])
a478 = Node(['4','7','8'])
a236 = Node(['2','3','6'])
a689 = Node(['6','8','9'])

a248.add_children([a478, a124, a268])
a268.add_children([a236, a689])

tree = Tree(a248)

print(max_w_indep_set(tree, graph))