import networkx as nx
from network2tikz import plot
from networkx.algorithms.traversal.depth_first_search import dfs_tree
from random import random
if __name__ == "__main__":
    G = nx.chordal_cycle_graph(120)
    subtree_at_2 = dfs_tree(G, 0, depth_limit=3)
    style = { }
    style['node_color'] = {}
    style['edge_color'] = {}
    style['edge_width'] = {}
    #style['force'] = {}
    style['edge_opacity'] = { e : 0.2 for e in G.edges() }
    style['layout'] = { u : (random()*9,  random()*6)  for u in G.nodes() }
    style['fixed'] = [ ]
    print(subtree_at_2.nodes())
    print(subtree_at_2.nodes())
    print(subtree_at_2.edges())

    _set = set()
    for j, (u,v) in enumerate(subtree_at_2.edges()):
        style['edge_opacity'][(u,v)] = 1
        style['edge_opacity'][(v,u)] = 1 
        style['edge_color'][(v,u)] = "black" 
        style['edge_color'][(u,v)] = "black" 
        
        if random() > 0.5:
            style['edge_color'][(u,v)] = "blue"

        style['fixed'].append(u)
        
        for z in [u,v]:
            if z not in _set:
                style['layout'][z] = ( 4 +  (random()-0.5)* (1 +len(_set)//3) , 10 + random()* (4 - len(_set)//5) )
                _set.add(z)
                style['node_color'][z] = "blue"  
                for e in G.adj[z]:
                    if random() > 0.5 :
                        style['edge_color'][(z,e)] = "blue" 
        
       # style['layout'][v] = (random()*(1 +j*0.5), 4 + random()*4)

    style["canvas"]=(7,15)
    style["keep_aspect_ratio"] = "False"
    #style["layout"] = "random" #"spring_layout"
    plot(G,'network2.tex', node_size = 0.1, **style )
    

