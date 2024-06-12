import math
from numpy.random import permutation as random_permutation
import random
import networkx
from functools import reduce
import networkx as nx
import matplotlib.pyplot as plt


def bipartite_regular_random_graph(n, m, d1, d2, seed=None, directed=False):
    """Return a random regular bipartite graph with d1,d2 left and right degree.

    Produces a regular bipartite graph chosen randomly out of the set of all graphs
    with n left nodes, m right nodes, and d1 left-degree and d2 right-degree. 

    If d1 * n does not equal to d2 * m, then exception is been raised.

    Parameters
    ----------
    n : int
        The number of nodes in the first bipartite set.
    m : int
        The number of nodes in the second bipartite set.
    d1 : int
        The degree of the any left vertex.
    d2 : int
        The degree of the any right vertex.
    seed : int, optional
        Seed for random number generator (default=None). 
    directed : bool, optional (default=False)
        If True return a directed graph 
        
    Examples
    --------
    G = nx.bipartite_regular_random_graph(10,20,3,4)

    See Also
    --------
    gnm_random_graph

    Notes
    -----

    """
    G = networkx.Graph()
    G=_add_nodes_with_bipartite_label(G,n,m)
    if directed:
        G=nx.DiGraph(G)
    G.name="bipartite_random_regular_graph(%s,%s,%s,%s)"%(n, m, d1, d2)
    if seed is not None:
        random.seed(seed)
    if n == 1 or m == 1:
        return G
    max_edges = n*m # max_edges for bipartite networks
    if d1*n >= max_edges or (d1*n != d2*m) : 
        raise Exception("Edges number is not consistent, d1*n != d2*m")

    left = [n for n,d in G.nodes(data=True) if d['bipartite']==0]
    right = list(set(G) - set(left))

    prefussion_edges = random_permutation(n*d1)
    #print(prefussion_edges)
    for i in range(n):
        for j in range(d1):
            G.add_edge(i, n + int(prefussion_edges[i*d1 + j]//d2) )
    return G


def _add_nodes_with_bipartite_label(G, lena, lenb):
    G.add_nodes_from(range(lena+lenb))
    b=dict(zip(range(lena),[0]*lena))
    b.update(dict(zip(range(lena,lena+lenb),[1]*lenb)))
    nx.set_node_attributes(G,b,'bipartite')
    return G



def count_right_intersection(G):
    def intersect(__list1, __list2):
        for a in __list1:
            if a in __list2:
                return True
        return False
    counter = 0
    left, right = nx.bipartite.sets(G)
    for v in right:
        for u in right:
            if u < v:
                if intersect(*(list(G.neighbors(_) for _ in [u,v]))):
                    counter+= 1
    return counter



if __name__ == "__main__":
    for n in [100, 200, 400, 800]:
        d1 = 3 
        m = int(n//5) 
        d2 = 15


        G = bipartite_regular_random_graph(n,m,d1,d2)
        #nx.draw(G, pos = nx.drawing.layout.bipartite_layout(G,nx.bipartite.sets(G)[0]))
        #nx.draw(G)
        #plt.draw()
        #plt.show()
        print(f"{n},{m},{count_right_intersection(G)}")


