
from pyx import *

from itertools import combinations, product, permutations
import numpy as np

from colorize_grids import *

from os import system


import math

def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])



def generate_complex(n):
    points = [ ]
    edges = [ ]
    for x in product( range(n), range(n), range(n) ):
        z = np.array(x)
        points.append( z ) 
        points.append( z + np.array([0.5, 0.5, 0.5]) )
        for (a,b,c) in permutations(np.eye(3), 3):
            for s in [1,-1]:
                vertices = [ z, z + a, z + (a + s*b + c)/2, z + (a + s*b - c)/2 ]
                for u,v in combinations(vertices,2):
                    edges.append( (u,v) ) 

    return points, edges

def hist_and_rotate_cells(cells, hist, axis, theta):
    rotation = rotation_matrix(axis, theta)
    return [  ( hist + rotation @ v for v in cell ) for cell in cells ] 

def tests():
    def inital_samll_grid(l=1):
        l = 2
        points, edges = generate_complex(l)
        c = canvas.canvas()
        N = 8
        edges = [ edges ] 
        for t in range(N):
            for tt in range(N):
                edges = edges + [ hist_and_rotate_cells(edges[0], np.array([2*(l+1) *(tt+1), 2*(l+2)*t ,0]), np.array( [ 1,1, 1 ]), ((t+tt+1)/(N*N))*7.2 ) ]
        for _edges in edges:
            for edge in _edges:
                projrct_edge_3dcolor_code(edge, c)
        c.writeSVGfile(f"3dcolor-{l}x{l}")


    def make_vido_small_grid(l = 1):
        points, edges = generate_complex(l)
        N = 120
        edges = [ edges ] 
        for t in range(N):

            edges = edges + [ hist_and_rotate_cells(edges[0], np.array([0, 0 ,0]), np.array( [ 1,1, 1 ]), (t/(N))*7.2 ) ]
        for t, _edges in enumerate(edges):

            c = canvas.canvas()
            for edge in _edges:
                projrct_edge_3dcolor_code(edge, c)
            c.writeSVGfile(f"3dcolor-{l}x{l}_{t}")
            system(f"convert 3dcolor-{l}x{l}_{t}.svg -alpha off 3dcolor-{l}x{l}_{t}.png")
            print(t)

        system(f"ffmpeg  -start_number 1 -i 3dcolor-{l}x{l}_%d.png -vcodec mpeg4 3dcolor-{l}x{l}.avi")
    #inital_samll_grid()
    make_vido_small_grid(l=3)

tests()
