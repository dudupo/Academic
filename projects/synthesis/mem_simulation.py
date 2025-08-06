from networkx import grid_graph
import networkx as nx
import matplotlib.pyplot as plt

import matplotlib.animation as animation
from random import random, shuffle
from copy import deepcopy 
import numpy as np

def n_grid(n, d):
    """n_grid.

    :param n:
    :param d:
    """
    return grid_graph(dim=( [n for _ in range(d)] ), periodic=True)


def random_assignment(G, p, assignment = None):
    """random_assignment.

    :param G:
    :param p:
    """
    f = lambda : 1 if random() < p else 0
    if assignment is None:
        return { edge : f() for edge in G.edges() }
    else:
        return { edge : f() ^ assignment[get_edge(assignment, edge)] for edge in G.edges() }

def shuffle_assignment(G, assignment):
    """random_assignment.

    :param G:
    """
    cedges = list(deepcopy(G.edges()))
    shuffle(cedges)
    return { rand_edge : assignment[get_edge(assignment, edge)] for rand_edge, edge in zip(cedges, G.edges()) }

def binary_number_generator(n):
    """binary_number_generator.

    :param n:
    """
    if n == 0:
        yield []
    else:
        for _num in binary_number_generator(n-1):
            yield [0] + _num 
            yield [1] + _num 

def binmul(H, vec):
    """binmul.

    :param H:
    :param vec:
    """
    n, m= len(H), len(H[0])
    ret = [ 0 for _ in range(n) ] 
    for i in range(n):
        for j in range(m):
            ret[i] ^= H[i][j] * vec[j]
    return ret 

def zero_vec(vec):
    """zero_vec.

    :param vec:
    """
    return sum(vec) == 0 

def create_local_code_given_chack_matrix(H):
    """create_local_code_given_chack_matrix.

    :param H:
    """
    n, m = len(H), len(H[0])
    Code = [ ] 
    for vec in binary_number_generator(m):
        u = binmul(H, vec)
        if zero_vec(u):
            Code += [vec]
    return Code

cashe = { }
def local_correction(bits, local_code):
    """local_correction.

    :param bits:
    :param local_code:
    """
    def hamming(x,y):
        """hamming.

        :param x:
        :param y:
        """
        return sum( [ 1 if _x != _y else 0 for _x,_y in zip(x,y) ] )  
    key = "".join( [str(_) for _ in bits] )
    if key not in cashe:
        cashe[key] = min( local_code , key = lambda x : hamming(x, bits ))
    return cashe[key]


def get_edge(_dict, edge):
    """get_edge.

    :param _dict:
    :param edge:
    """
    x,y = edge
    if edge in _dict:
        return edge
    elif (y,x) in _dict:
        return y,x
    else:
        return 0
        


def Tanner_correction(G, assign, Code):
    """Tanner_correction.

    :param G:
    :param assign:
    :param Code:
    """
    nodes = [ _ for _ in G.nodes() ]
    shuffle(nodes)
    for node in nodes:
        bits = [ assign[ get_edge(assign, edge)] for edge in G.edges(node)]
        new_assign = deepcopy(assign)
        correction = local_correction(bits, Code)
        for i, edge in enumerate(G.edges(node)):
            edge = get_edge(assign, edge)
            new_assign[edge] = correction[i]
    return new_assign

def rep_code_matrix(D):
    """rep_code_matrix.

    :param D:
    """
    H = [ [ 0 for _ in range(D) ] for _ in range(D) ] 
    for i in range(D):
        H[i][i], H[i][(i+1)%D] = 1, 1
    return create_local_code_given_chack_matrix(H)



def small_visual_gif(Graph, local_code, file_name='sim.gif' , noise_rate=0.3, frames=40):
    """small_visual_gif.

    :param Graph:  The graph on which the tanner code is defined in networkx.
    :param local_code: List of valid code words on the local view of the vertices.
    :param file_name: Path to save the gif. 
    :param noise_rate: Either a portion (flaot number in [0,1]) or an assignment of bits on the edges (error), defined as dictionary between edges to bits.
    :param frames: Number of frames. 
    """

    assign = random_assignment(Graph, noise_rate) if isinstance(noise_rate, float) else noise_rate
    assign_time = [ assign ]
    for _ in range(frames):
        assign_time += [ Tanner_correction(Graph, assign_time[_], local_code) ]

    fig, ax = plt.subplots(figsize=(20, 20))
    pos = nx.spring_layout(Graph)

    def update(frame):
        """update.

        :param frame:
        """
        ax.clear()
        nx.draw(Graph, pos, node_size=[0.1 for node in Graph.nodes()], ax=ax)
        nx.draw_networkx_edge_labels(Graph, pos, edge_labels=assign_time[frame], bbox=dict(alpha=0), ax=ax)
    ani = animation.FuncAnimation(fig=fig, func=update, frames=frames, interval=100) # repeat=False)
    ani.save(file_name, fps=30)


def Graph_visulation(Graph, local_code, file_name='sim.gif' , noise_rate=0.3, frames=20, permu=False):
    """Graph_visulation
    :param Graph:  The graph on which the tanner code is defined in networkx.
    :param local_code: List of valid code words on the local view of the vertices.
    :param file_name: Path to save the gif. 
    :param noise_rate: Either a portion (flaot number in [0,1]) or an assignment of bits on the edges (error), defined as dictionary between edges to bits.
    :param frames: Number of frames. 
    """


    assign = random_assignment(Graph, noise_rate) if isinstance(noise_rate, float) else noise_rate
    assign_time = [ assign ]
    for _ in range(frames):
        print(_)
        assign_time += [ Tanner_correction(Graph, assign_time[-1], local_code) ]
        #assign_time += [ random_assignment(Graph, noise_rate, assign_time[-1]) ]
        if permu:
            assign_time += [ shuffle_assignment(Graph,  assign_time[-1]) ]
        else: 
            assign_time += [  assign_time[-1] ] 
    error_size = [  ] 
    n = len(assign.values())
    for frame in assign_time:
        error_size += [ float(sum(frame.values()))/ n ]

    return np.array(error_size)
    #plt.plot(error_size)

if __name__ == "__main__":

    D = 3
    Code = rep_code_matrix(2*D)
    print(Code)

    G = n_grid(5, D)
    exps = 50 
    errors_1 = (1/exps) * Graph_visulation(G, Code, noise_rate=0.05, permu=True)
    errors_2 = (1/exps) * Graph_visulation(G, Code, noise_rate=0.05)

    for _ in range(exps-1):
        errors_1 += (1/exps) * Graph_visulation(G, Code, noise_rate=0.05, permu=True)
        errors_2 += (1/exps) * Graph_visulation(G, Code, noise_rate=0.05)
    
    plt.plot(errors_1, label="with permuations")
    plt.plot(errors_2, label="without permutations")
    plt.legend( [ "with permuations", "without permutations"] )
    plt.show()

    #exit(0)
  #  small_visual_gif(G, Code, noise_rate=0.3, frames = 70)
   
   # exit(0)
