import networkx as nx
#from network2tikz import plot
from networkx.algorithms.traversal.depth_first_search import dfs_tree
from random import random
if __name__ == "__main__":
    G = nx.random_regular_graph(3,120) # nx.path_graph(120)  #nx.chordal_cycle_graph(120)
    subtree_at_2 = dfs_tree(G, 0, depth_limit=2)
    style = { }
    style['node_color'] = {}
    style['edge_color'] = {}
    style['edge_width'] = {}
    #style['force'] = {}
    style['edge_opacity'] = { e : 0.2 for e in G.edges() }
    style['layout'] = { u : (  8 + random()*6 , random()*12 )  for u in G.nodes() }
    node_label =     { u : "" for u in G.nodes() } 
    style['fixed'] = [ ]
    print(subtree_at_2.nodes())
    print(subtree_at_2.nodes())
    print(subtree_at_2.edges())

    _set = set()
    for j, (u,v) in enumerate(subtree_at_2.edges()):
        #style['edge_opacity'][(u,v)] = 1
        #style['edge_opacity'][(v,u)] = 1 
        #style['edge_color'][(v,u)] = "black" 
        #style['edge_color'][(u,v)] = "black" 
        
        #if random() > 0.5:
        #    style['edge_color'][(u,v)] = "blue"

        style['fixed'].append(u)
        
        for z in [u,v]:
            if z not in _set:
                style['layout'][z] = ( 1 + 0.2 *(j-4.5)**2  , 3 + 0.5*j ) if j > 0 else ( 0 , 5)
                _set.add(z)
        #        style['node_color'][z] = "blue"  
                for e in G.adj[z]:
                    if random() > 0.5 :
                        pass 
                 #       style['edge_color'][(z,e)] = "blue" 
        
       # style['layout'][v] = (random()*(1 +j*0.5), 4 + random()*4)

    style["canvas"]=(16,10)
    #style["keep_aspect_ratio"] = "False"
    #style["layout"] = "random" #"spring_layout"
    nx.write_latex(G, 'network2.tex', pos = style['layout'], tikz_options="[scale=1]", node_options = { u : "[shape=circle,draw=black]" for u in G.nodes() }, node_label=node_label, default_edge_options = "[draw opacity=0.5]") 
#open('network2.tex', 'w').write(G.to_latex(pos=style['layout']) )
#\begin{tikzpicture}
#\draw (0,0) -- (2,2);
#\end{tikzpicture}
    

