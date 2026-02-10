
from pyx import *
import numpy as np
from itertools import combinations, product
from copy import deepcopy
from random import random, shuffle, choice, sample
import matplotlib.pyplot as plt
import gc

from operator import __add__ , __sub__
from multiprocessing import Pool 


DEBUG = False
DEBUG2 = True

def diff_referance(bit, u, n, op=__sub__):
    return tuple( tuple( op(x,y) % n for x,y in zip(v,u) ) for v in bit )
def diff_referance_bits(bits, u, n, op=__sub__):
    return [ diff_referance(bit, u, n, op=op) for bit in bits ]

def _direct(i,k):
    ret = np.zeros(k, dtype=int)
    ret[i] = 1
    return ret

def directions_vec(k):
    return [ _direct(i, k)  for i in range(k) ]

def local_gen(local_bits):
    for binary_assignment in product([0,1], repeat = len(local_bits)):
        yield binary_assignment 

def cells_neighbourhood( k, vertex = None, sign=True, celldim=2, _filter = lambda x : True ) :

    def totuple( vec ):
        return tuple( i for i in vec ) 

    directions = directions_vec(k)
    vertex = np.zeros(k, dtype=int) if vertex == None else  np.array(vertex, dtype=int)
    ret = [ ]
    for generators in combinations( range(k), celldim):
        signs = filter(_filter, product([-1,1], repeat=celldim)) if sign else [  (1,1) ]
        for sign_conf in signs:
            left, right = deepcopy(vertex), deepcopy(vertex)
            for sign_i, gen_i in zip(sign_conf, generators):
                if sign_i == -1:
                    left  -= directions[gen_i]
                else:
                    right += directions[gen_i]
            ret += [ ( totuple(left), totuple(right) ) ] 
    return ret



def faces_vec(k, vertex = None, sign=True, celldim=2):
    '''
        faces_vec, Given vertex and a cell-dim returns all
        the cells on the vertex's local view.
    '''
    return cells_neighbourhood(k, vertex=vertex, sign=sign, celldim=celldim)


def positive_time_cells_on_vertex(k, vertex = None, sign=True , celldim =2):
    '''
        positive_time_cells_on_vertex, takes the 
    '''
    _filter = lambda x : sum(x) > 0 
    return cells_neighbourhood(k, vertex=vertex, sign=sign, celldim=celldim, _filter = _filter)


def positive_time_checks_on_vertex(k, vertex = None, sign=True , checksdim = 0):
    '''
        positive_time_cells_on_vertex, takes the 
    '''
    _filter = lambda x : sum(x) > 0 
    return cells_neighbourhood(k, vertex=vertex, sign=sign, celldim=checksdim, _filter = _filter)

def Zgenrators_for_3D_cells_on_faces_checks_on_edges(n):
    k, celldim, checksdim = 3, 2, 1
    origin = (0,0,0)
    positive_cells  = cells_neighbourhood(k, celldim=celldim, _filter = lambda x : sum(x) > 0)
    positive_checks = cells_neighbourhood(k, celldim=checksdim, _filter = lambda x : sum(x) > 0)

    def progress_face_by_g(face, generator, times):
        return tuple( tuple(x + times*y for  x,y in zip(v,generator)) for v in face)
    
    Zgenerators = []
    for i in range(3):
        Zgenerators.append([])
        for _ in range(n):
            Zgenerators[-1].append(progress_face_by_g(positive_cells[i], positive_checks[(i+2) % 3][-1], _))

    return Zgenerators

def check_X_generators(grid, assignment):
    if (grid.k != 3) or (grid.celldim != 2) or (grid.checksdim != 1):
        raise Exception('Not 3D toric, checks should be set on the edges') 
    temp_assignment = deepcopy(assignment)
    counter = 0 
    while(grid.syndrom_size(temp_assignment) > 0):
        temp_assignment = grid.correction_cycele_swift_rule(temp_assignment)
        counter += 1
        if counter > (grid.n ** 3):
            print("2,2,2")
            return [2,2,2]
    ret = [0,0,0]

    if DEBUG2:
        taken = set( )

    for j,zgen in enumerate(Zgenrators_for_3D_cells_on_faces_checks_on_edges(grid.n)):
        for bit in zgen:
            if DEBUG2:
                if grid.on_the_grid(bit, req_depth=2) in taken:
                    raise Exception('take duplicate bit for parity')
                taken.add( grid.on_the_grid(bit, req_depth=2) )
            ret[j] ^= temp_assignment[grid.on_the_grid(bit, req_depth=2)]
    return ret



def sample_3_connected_bits(grid, sym=False):
    if sym:
        stabilizer = list(grid.checks.keys())[0]
    else:
        stabilizer = choice(list(grid.checks.keys()))
    return sample(grid.checks_to_bits[stabilizer], 3)


class KDgrid:
    def __init__(self, n, k, celldim=2, checksdim =0, diff = 0):
        self.n, self.k = n, k
        self.diff = diff 
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


        self.cache_table = { }
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
        
        self.vertex_to_positive_bits = { }
        self.vertex_to_positive_checks = { }
        self.vertex_to_checks = { }
        self.vertex_to_local_view_bits = { }

        self.debug_picked = [ ]

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
    def get_syndrom(self, assignment):
        ret = []
        for u in self.checks.keys():
            if self.local_syndrom(u, assignment) != 0:
                ret.append(u)
        return ret

    def local_correaction(self, face, assignment):
        stabilizers = self.bits_to_checks[face]
        syndrom_diff = 0
        for stabilizer in stabilizers:
            syndrom_diff += { 0 : 1 , 1 : -1}[self.local_syndrom(stabilizer, assignment)]
        return syndrom_diff < self.diff

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
        self._colors = _colors
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
    
    def correction_cycele_max_color(self, assignment):
        _maxcolor, _maxdecrease, ret = 0, 0, assignment
        last_syndrom = self.syndrom_size(assignment)
        for color in range(self._colors): 
            suggested_correction = self.local_correaction_group(self.colorized_dic[color], deepcopy(assignment))
            syndrom_diff = last_syndrom - self.syndrom_size(suggested_correction) 
            if (color ==0) or ( _maxdecrease < syndrom_diff):
                _maxdecrease, ret = syndrom_diff, suggested_correction 
            #else:
                #del suggested_correction
                #gc.collect()
        return ret


    def correction_cycele_all_take_maj(self, assignment):
        return self.local_correaction_group(assignment.keys(), assignment)

    def correction_cycele_random_pair(self, assignment):
        return self.local_correaction_group(self.zbits.keys() ,assignment,  local_decoder = self.local_correaction_D_random_pick)

    

    def correction_cycele_swift_rule(self, assignment):

        self.debug_picked = [ ]


        #def diamond_contained(bits, checks):
            #bits_diamond = self.face_to_vertex(

        def swift_vertex(vertex):
            if vertex not in self.vertex_to_positive_bits:
                bits =  [self.on_the_grid( cell, req_depth=2) for cell in
                            positive_time_cells_on_vertex(
                                self.k, vertex = vertex, celldim = self.celldim)]
                self.vertex_to_positive_bits[vertex] = bits
            else:
                bits = self.vertex_to_positive_bits[vertex]

            if vertex not in self.vertex_to_positive_checks:
                checks = [self.on_the_grid( cell, req_depth=2) for cell in
                            positive_time_checks_on_vertex(
                                self.k, vertex = vertex, checksdim = self.checksdim )]
                all_checks_around_vertex =  [self.on_the_grid( cell, req_depth=2) for cell in
                            faces_vec( self.k, vertex = vertex, celldim = self.checksdim )]


                self.vertex_to_positive_checks[vertex] = checks
                self.vertex_to_checks[vertex] = all_checks_around_vertex
            else:
                checks = self.vertex_to_positive_checks[vertex]
                all_checks_around_vertex = self.vertex_to_checks[vertex] 
            
            

            all_local_checks = set(sum([ self.bits_to_checks[bit] for bit in bits ], start=[]))
            not_positive_checks = set(all_checks_around_vertex)- set(checks)


            local_view_syndrom = tuple( ( diff_referance(check, vertex, self.n), self.local_syndrom(check, assignment ) ) for 
                                        check in all_local_checks)

            sig = local_view_syndrom

            temp_assignment, temp_syndrom = assignment, 0
            last_local_syndrom = 0
            syndrom_word = [ ] 
            for check in checks:
                temp = self.local_syndrom(check, temp_assignment)
                syndrom_word.append(temp)
                last_local_syndrom += temp

            picked = [0] * len(bits)
            trailing = last_local_syndrom > 0 #(all(self.local_syndrom(check, temp_assignment) == 0 for check in not_positive_checks)) and  (last_local_syndrom > 0)
            if trailing:
                if sig in self.cache_table:
                    return self.cache_table[sig]
                
                #print(f"trailing - {sig}")
                for binary_assignment in product([0,1], repeat = len(bits)):
                    if DEBUG:
                        if 1 in syndrom_word:
                            print(f"domain wall {syndrom_word}")
                            print( f"\t\t[>] {vertex}, {binary_assignment}")
                    in_domain_wall = True
                    for bit, value in zip(bits, binary_assignment):
                        temp_assignment[bit] ^= value

                    for j, check in enumerate(checks):
                        check_syndrom = self.local_syndrom(check, temp_assignment)
                        if check_syndrom != 0: # syndrom_word[j]:
                            in_domain_wall = False
                        temp_syndrom += check_syndrom

                    if in_domain_wall:
                        if temp_syndrom <= last_local_syndrom:
                            if temp_syndrom != 0:
                                raise Exception(f'syndrom:{temp_syndrom}')
                            if (temp_syndrom < last_local_syndrom) or (sum(binary_assignment) < sum(picked)): 
                                last_local_syndrom = temp_syndrom
                                picked = binary_assignment

                    for bit, value in zip(bits, binary_assignment):
                        temp_assignment[bit] ^= value
                    temp_syndrom = 0
                self.cache_table[sig] = list(zip( diff_referance_bits(bits, vertex, self.n), picked))
                if DEBUG:
                    if 1 in syndrom_word:
                        print(f"domain wall {syndrom_word}")
                        print( f"\t\t[p] {vertex}, {picked}")
                return self.cache_table[sig]
                #return list(zip( diff_referance_bits(bits, vertex, self.n), picked))
            else:
                return list(zip( diff_referance_bits(bits, vertex, self.n), picked))

      
        gens, ret_assign = [], deepcopy(assignment)
        assigned = set()
        for vertex in self.vertices:
            for rbit, value in swift_vertex(vertex):
                bit = diff_referance(rbit, vertex, self.n, op=__add__)
                if DEBUG:
                    if value == 1:
                        self.debug_picked.append(bit)
                    if bit in assigned:
                        raise Exception()
                    assigned.add(bit)
                ret_assign[bit] ^= value

        not_assigned = set()
        
        if DEBUG:
            for bit in self.zbits.keys():
                if bit not in assigned:
                    not_assigned.add(bit)
            if len(not_assigned) > 0:
                print("#####################################################")
                print("\n".join( str(x) for x in not_assigned))
                raise Exception(f'no value were assigned') 

        return ret_assign

    def stabilizers_iterator(self, count=100):
        m = len(self.checks.items())
        
        logic_stabilizers = [  [ choice([0,1]) for _ in range(m) ] for __ in range(count) ]

        for logic_stabilizer in logic_stabilizers:
            ret = deepcopy(self.zbits)
            for i, check in zip(logic_stabilizer, self.checks.keys()):
                for bit in self.checks_to_bits[ check ]: 
                    if i == 1:
                        ret[bit] ^= 1

            yield ret


'''

        # -------------------- Multi processing -------------------- #
        ret_assign = deepcopy(assignment)
        restuls = [ ]

        def swift_chunk(chunk):
            ret = [ ]
            for vertex in chunk:
                ret += [ swift_vertex(vertex) ]
            return ret

        def split_chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]

        processes_number = 30
        with Pool(processes = processes_number) as pool:
            gens = internal_func_map(pool, swift_chunk, [ list(chunk) for chunk in split_chunks(self.vertices, processes_number) ])
            result = sum( gens, start = [])
            for _gen in result:
                for bit, value in _gen:
                    ret_assign[bit] ^= value
        return ret_assign
        # -------------------- Multi processing -------------------- #

import marshal
import multiprocessing
import types
from functools import partial

def internal_func_map(pool, f, gen):
    marshaled = marshal.dumps(f.__code__)
    return pool.map(partial(run_func, marshaled=marshaled), gen)


def run_func(*args, **kwargs):
    marshaled = kwargs.pop("marshaled")
    func = marshal.loads(marshaled)

    restored_f = types.FunctionType(func, globals())
    return restored_f(*args, **kwargs)
'''

class FingerPrint(dict):
    def __init__(self, *arg, **kw):
        self.tracking = False
        self.tupped = set( )
        super(FingerPrint, self).__init__(*arg, **kw)
       

    def __getitem__(self, key):
        if self.tracking:
            self.tupped.add(key)
        return super(FingerPrint, self).__getitem__(key)
    def start_track(self):
        self.tracking = True
        self.tupped = set( )
    def get_tracks(self):
        self.tracking = False
        return list(self.tupped)

cache_light_cone = { }
def test_hypotesis( ):

    def single_test(grid, p, cond = False):
        x,y,z = sample_3_connected_bits(grid, sym = True)
        
        if (x,y) in cache_light_cone:
            light_cone = cache_light_cone[(x,y)]
        elif (y,x) in cache_light_cone:
            light_cone = cache_light_cone[(y,x)]
        else:
            temp = FingerPrint( deepcopy(grid.zbits) ) 
            temp.start_track()
            grid.local_correaction_group( [x,y] , temp) 
            light_cone = { bit : 0 for bit in temp.get_tracks() }
            cache_light_cone[(x,y)] = light_cone

        assign = grid.random_assignment(p, assignment = deepcopy(light_cone))
        if cond and z in light_cone:
            assign[z] = 1
        if (not cond) and z in light_cone:
            assign[z] = 0
        assign = grid.local_correaction_group( [x,y] , assign) 
        if assign[x] == 0 and assign[y] == 0:
            return 0
        return 1

    grid = KDgrid(4,4, checksdim =1)
    
    
    attempts = 1000

    p0, p1, ps = [], [], list(np.linspace(0.001, 0.0025, num = 50))
    for p in ps:
        print(p)
        p0x, p1x = 0, 0
        for i in range(attempts):
            if i % 1000 == 0:
                print(i)
            p0x += single_test(grid, p)
            p1x += single_test(grid, p, cond = True)
        p0x, p1x = p0x/attempts, p1x/attempts
        p0.append(p0x)
        p1.append(p1x)
    
    eps = 0 #0.01
    p2 = [ p**(2+eps) for p in ps ] 
    #p2 = [ p for p in ps ] 
    plt.plot(ps, p0)
    #plt.plot(ps, p1)
    plt.plot(ps, p2)
    #plt.ylim(0, 4*1e-5)
    plt.show()



if __name__ == "__main__":

    test_hypotesis()

    #print(len(Zgenrators_for_3D_cells_on_faces_checks_on_edges(29)[0]))
    #print(Zgenrators_for_3D_cells_on_faces_checks_on_edges(30)[0])

    
#    for i, stab in enumerate(grid.stabilizers_iterator(count=100)):
#        r = sum(stab.values())
#        print(f'{i} := {r}, {r%4}')
