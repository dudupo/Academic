import networkx as nx
#from network2tikz import plot
from networkx.algorithms.traversal.depth_first_search import dfs_tree
from random import random
import numpy as np
if __name__ == "__main__":
    G = nx.cycle_graph(30) # nx.path_graph(120)  #nx.chordal_cycle_graph(120)
    subtree_at_2 = dfs_tree(G, 0, depth_limit=2)
    style = { }
    style['layout'] = { u : (  4* np.cos( j/30 * 2 * np.pi)  , 4 * np.sin( j/30 * 2 * np.pi)  )  for j,u in enumerate(G.nodes()) }
    node_label =     { u : "" for u in G.nodes() } 
    _set = set()
    nx.write_latex(G, 'network2-cycle.tex', pos = style['layout'], tikz_options="[scale=1]", node_options = { u : "[shape=circle,draw=black]" for u in G.nodes() }, node_label=node_label, default_edge_options = "[draw opacity=0.5]", edge_label = { w : "$1$" for w in G.edges()} ) 
#open('network2.tex', 'w').write(G.to_latex(pos=style['layout']) )
#\begin{tikzpicture}
#\draw (0,0) -- (2,2);
#\end{tikzpicture}
    

