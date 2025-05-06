import numpy as np
from itertools import product
import networkx as nx
import matplotlib.pyplot as plt

import matplotlib as mpl

mpl.rcParams['font.size'] = 20
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = r'\usepackage{{amsmath}}'

def iterate_binary_matrices(n=5):
    total = 2 ** (n * n)
    for bits in range(total):
        # Convert bits to binary matrix
        binary_string = f'{bits:0{n*n}b}'
        matrix = np.array([int(b) for b in binary_string]).reshape((n, n))
        if len(np.linalg.eigvals(matrix)) == n: 
            yield bits, matrix

def Hamming(M1, M2):
    count = 0 
    for i in range(len(M1)):
        for j in range(len(M1)):
            if M1[i][j] != M2[i][j]:
                count += M1[i][j]
    return count 

def interlacing(M1, M2):
    eigenvalues_1 = sorted(np.linalg.eigvals(M1))
    eigenvalues_2 = sorted(np.linalg.eigvals(M2))
    for i in range(len(eigenvalues_1)):
        if eigenvalues_1[i] >= eigenvalues_2[i]:
            return False
    return True

def make_graph(n = 5):
    vertices = list( iterate_binary_matrices(n) )
    edges = [ ] # [ [] for _ in range(len(vertices) )]
    rankone = [ ]
    for i, v in vertices:
        for j, g in vertices:
            if  i != j: # and
                if interlacing(v,g):
                    edges.append((i,j))
                    if  Hamming(v,g) == 1:
                        rankone.append( (i,j))
    return vertices, edges, rankone 
def compute_eigenvalues(n=5, max_matrices=None):
    results = []
    for i, matrix in enumerate(iterate_binary_matrices(n)):
        results.append((matrix, eigenvalues))
        if max_matrices and i + 1 >= max_matrices:
            break
    return results

def bmatrix(a):
    """Returns a LaTeX bmatrix

    :a: numpy array
    :returns: LaTeX bmatrix as a string
    """
    if len(a.shape) > 2:
        raise ValueError('bmatrix can at most display two dimensions')
    lines = str(a).replace('[', '').replace(']', '').splitlines()
    rv = [r'\begin{bmatrix}']
    rv += ['  ' + ' & '.join(l.split()) + r'\\' for l in lines]
    rv +=  [r'\end{bmatrix}']
    return  "$" + ' '.join(rv) + "$"

def plot_graph(vertices, edges, r, directed=False):
    # Create a graph object
    G = nx.DiGraph() if directed else nx.Graph()
    #plt.figure(num=None, figsize=(40, 40), dpi=80)        
    labels = { _ : bmatrix(v) for (_,v) in vertices } 

    # Add nodes and edges
    G.add_nodes_from(vertices)
    G.add_edges_from(edges)
    # Draw the graph
    for layer, nodes in enumerate(nx.topological_generations(G)):
        for node in nodes:
            G.nodes[node]["layer"] = layer

    pos = nx.multipartite_layout(G, subset_key="layer")
    fig, ax = plt.subplots()
    nx.draw_networkx(G, pos=pos, ax=ax)
    nx.draw_networkx_labels(G, pos, labels, font_size=22)
    
    #pos = nx.spring_layout(G)  # Positions for all nodes
    #nx.draw_circular(G, with_labels=True, node_color='lightblue', edge_color='gray', node_size=20, font_size=12)
    plt.title("Graph Visualization")
    plt.savefig('graph.png')

# Example usage - be careful with large number of matrices
if __name__ == "__main__":
    # Set max_matrices to limit, or None for full iteration (takes hours!)

    V,E, r= make_graph(2)
    plot_graph( V, E,r,  True)
    
