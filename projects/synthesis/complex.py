
from pyx import *
import numpy as np
from itertools import combinations, product
from copy import deepcopy
from random import random, shuffle, choice, sample
import matplotlib.pyplot as plt

def _direct(i,k):
    ret = np.zeros(k, dtype=int)
    ret[i] = 1
    return ret

def directions_vec(k):
    return [ _direct(i, k)  for i in range(k) ]

def faces_vec(k, vertex = None, sign=True, celldim=2):
    '''
        faces_vec, Given vertex and a cell-dim returns all
        the cells on the vertex's local view.
    '''
    def totuple( vec ):
        return tuple( i for i in vec ) 

    directions = directions_vec(k)
    vertex = np.zeros(k, dtype=int) if vertex == None else  np.array(vertex, dtype=int)
    ret = [ ]
    for generators in combinations( range(k), celldim):
        signs = product([-1,1], repeat=celldim) if sign else [  (1,1) ]
        for sign_conf in signs:
            left, right = deepcopy(vertex), deepcopy(vertex)
            for sign_i, gen_i in zip(sign_conf, generators):
                if sign_i == -1:
                    left  -= directions[gen_i]
                else:
                    right += directions[gen_i]
            ret += [ ( totuple(left), totuple(right) ) ] 
    return ret


class KDgrid:
    def __init__(self, n, k, celldim=2, checksdim =0):
        self.n, self.k = n, k
        self.celldim, self.checksdim = celldim, checksdim
        self.vertices = list( product(range(n), repeat=k) )
     
        self.zbits = { } 
        self.checks = { }

        for u in list( product(range(n), repeat=k) ):
            for face in self.faces_vec(vertex=u, sign=False):
                _face = tuple(self.on_the_grid(face, req_depth=2))
                self.zbits[_face] = 0 
        
        for u in list( product(range(n), repeat=k) ):
            for check in self.checks_vec(vertex=u, sign=False):
                _check = tuple(self.on_the_grid(check, req_depth=2))
                self.checks[_check] = 0 


        self.face_to_vertex = { }
        self.views = { }
        self.check_to_vertex = { }
        self.check_views = { }
        for views_map, inverse_map, func in zip( [self.views, self.check_views], [self.face_to_vertex, self.check_to_vertex], [self.faces_vec, self.checks_vec]):
            for u in list( product(range(n), repeat=k) ):
                views_map[u] = [ ]
                for face in func(vertex=u, sign=True):
                    _face = tuple(self.on_the_grid(face, req_depth=2))
                    views_map[u].append(_face) 
                    if _face not in inverse_map:
                        inverse_map[_face] = []
                    inverse_map[_face].append( self.on_the_grid(u, req_depth=1)  )
#------------------------- generalized Toric ------------------------------------------# 
        self.bits_to_checks = { bit:   [] for bit in self.zbits.keys() }
        self.checks_to_bits = { check: [] for check in self.checks.keys() }

        if self.celldim > self.checksdim:
            lowcells = self.checks.keys()
            high_to_low, low_to_high = self.bits_to_checks, self.checks_to_bits
            v_to_high = self.views
        else:
            lowcells = self.zbits.keys()
            high_to_low, low_to_high =  self.checks_to_bits, self.bits_to_checks
            v_to_high = self.check_views

        for left, right in lowcells:
            for face_i in v_to_high[left]:
                for face_j in v_to_high[right]:
                    if face_i == face_j:
                        low_to_high[ (left, right)].append( face_i )
                        high_to_low[ face_i ].append((left, right))
#------------------------- generalized Toric ------------------------------------------# 

        self.colorized_dic = self.get_colorized()

    def _direct(self, i):
        return _direct(i, self.k)

    def directions_vec(self):
        return directions_vec(self.k)

    def faces_vec(self, vertex = None, sign=True):
        return faces_vec(self.k, vertex = vertex, sign=sign, celldim = self.celldim)
    
    def checks_vec(self, vertex = None, sign=True):
        return faces_vec(self.k, vertex = vertex, sign=sign, celldim = self.checksdim)

    def on_the_grid(self, obj, req_depth=1, _copy = False): 
        if req_depth == 1:
            obj = tuple([ v % self.n for v in obj ])
        else:
            obj = tuple( [self.on_the_grid(sub_obj, req_depth = req_depth-1, _copy=_copy) for  sub_obj in obj ] )
        return obj
    
    def get_zerobits(self):
        return deepcopy(self.zbits)


    def random_assignment(self, p, assignment = None):
        """random_assignment.

        :param G:
        :param p:
        """
        f = lambda : 1 if random() < p else 0
        if assignment is None:
            return { key : f() for key in self.zbits.keys() }
        else:
            for key,val in assignment.items():
                assignment[key] ^= f()
            return assignment
            #return { key : f() ^ assignment[key] for key in self.get_zerobits().keys() }


    def local_syndrom(self, _check, assignment):
        bits = self.checks_to_bits[_check]
        parity = 0 
        for bit in bits:
            parity ^= assignment[bit]
        return parity

    def syndrom_size(self, assignment):
        ret = 0
        for u in self.checks.keys():
            ret += self.local_syndrom(u, assignment)
        return ret


    def local_correaction(self, face, assignment):
        stabilizers = self.bits_to_checks[face]
        syndrom_diff = 0
        for stabilizer in stabilizers:
            syndrom_diff += { 0 : 1 , 1 : -1}[self.local_syndrom(stabilizer, assignment)]
        return syndrom_diff < 0

    def local_correaction_D_random_pick(self, face, assignment):
        random_stabilizers_pair = sample(self.bits_to_checks[face], 2)
        syndrom_diff = 0
        for stabilizer in random_stabilizers_pair:
            syndrom_diff += { 0 : 1 , 1 : -1}[self.local_syndrom(stabilizer, assignment)]
        return syndrom_diff == -2

    def local_correaction_group(self, faces, assignment, local_decoder = None ):
        if local_decoder is None:
            local_decoder=self.local_correaction
        flipped = { face : False for face in faces  }
        for face in faces:
            flipped[face] = local_decoder(face, assignment)
        for face in faces:
            if flipped[face]:
                assignment[face] ^= 1
        return assignment
  


    def get_colorized(self):
        def random_color(colors):
            return {  face : choice( range(colors)  ) for face in  self.zbits.keys()}
        _colors = 32
        colorized = random_color(_colors)
        colorized_dic = { _ : [] for _ in range(_colors) }
        for face in self.zbits.keys():
            notseen = [ True ] * _colors
            notseen[colorized[face]] = False
            for stabilizer in self.bits_to_checks[face]:
                for facej in self.checks_to_bits[stabilizer]:
                    #if facej not in colorized:
                        #facej = facej[-1],facej[0]
                    if (facej != face) and (colorized[face] ==  colorized[facej]):
                        for j, _notseen in enumerate(notseen):
                            if _notseen:
                                colorized[face] = j
                                notseen[j] = False
                                break
                    notseen[colorized[facej]] = False
            colorized_dic[colorized[face]].append(face)  
        return colorized_dic

    def correction_cycele(self, assignment, color=0):
        return self.local_correaction_group(self.colorized_dic[color], assignment)
    
    def correction_cycele_all_take_maj(self, assignment):
        return self.local_correaction_group(assignment.keys(), assignment)

    def correction_cycele_random_pair(self, assignment):
        return self.local_correaction_group(self.zbits.keys() ,assignment,  local_decoder = self.local_correaction_D_random_pick)

    


