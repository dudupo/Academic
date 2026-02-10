

from pyx import *
import numpy as np
from itertools import combinations, product
from copy import deepcopy
from random import random, shuffle, choice
import matplotlib.pyplot as plt

from os import system
import os
from complex import *
from colorize_grids import *
from multiprocessing import Process, Array

from pickle import dump, load 
import datetime

def correlation_test( ):
    plt.clf()
   
    p = 0.1
    def run(grid):
        Time = 20
        assign = grid.random_assignment(p, assignment = None)
        for t in range(Time):
            assign = grid.correction_cycele_swift_rule(assign)
            assign = grid.random_assignment(p, assignment = assign)
        return assign

    
    N, n = 40, 100
    grid = KDgrid(n,2, celldim=2, checksdim=1)

    for _ in range(N):
        outcome = run(grid)
        dump( outcome, open(f"raw-{n}-{p}-{datetime.datetime.now()}.pkl", "wb"))  

def load_pkl( ):
    pickles = {}
    for filename in os.listdir('.'):
        if filename.endswith('.pkl') or filename.endswith('.pickle'):
            with open(filename, 'rb') as f:
                print(f)
                pickles[filename] = load(f)

    #for pkl in pickles.values():
    #   print(pkl)
    
    
    def check_S(S, assign):
        for bit in S:
            if assign[bit] == 0:
                return 0
        return 1

    def track_over(grid):
        return [ [ list(grid.zbits.keys())[0],  list(grid.zbits.keys())[1]] ]

#    S = track_over(grid)
#    histS = [ 0 for s in S ]
#    for i, s in enumerate(S):
#            histS[i] += check_S(s, outcome)
#    for i, s in enumerate(S):
#        histS[i] /= N
#    print( [S, histS])
#    dump( [S, histS], open(f"exp-{datetime.datetime.now()}.pkl", "wb"))  
    

def span(subset, k):
    # subset : a list of k-tuple coordinates. 
    funcs = [ ]
    ret = 0
    for _ in range(k):
        ret -= min(subset, key = lambda x : x[_])[_]
    ret += sum(max(subset, key = lambda x : sum(x)))
    return ret

def span_step(origin, subset, k):
    flags = [ False for _ in range(k+1) ]
    for _ in range(k):
        for point in subset: 
            if point[_] >= origin[_]:
                flags[_] = True
    for point in subset: 
        if (sum(point) + 1) <= sum(origin):
            flags[-1] = True
    return all(flags)

def test_span():
    print("[test]test_span:")
    print( span( [ (0,0), (0,5), (5,0), (1,1), (1,2) ], 2) == 5 )
    print( span( [ (0,0,0), (0,5,0), (5,0,0), (1,1,0), (1,2,0) ], 3) == 5 )
    print( span( [ (0,0,1), (0,5,0), (5,0,0), (1,1,0), (1,2,0) ], 3) == 5 )
    print( span( [ (0,0,1), (0,5,1), (5,1,0), (1,1,0), (1,2,0) ], 3) == 5 )

def coordiantes_of_k_faces(faces, k):
    def center_of_face(face):
        u,v = face
        return tuple( 0.5* (z + w) for z,w in zip(u,v) )

    subset = [ center_of_face(face) for face in faces ]
    return subset

def check_spanning_growth_toric(dimension):
    grid = KDgrid(3, dimension, celldim=2, checksdim=1)
    temp_assignment = deepcopy(grid.zbits)
    zero_vertex = tuple( 1 for _ in range(dimension) ) # (1,1,1,..)
    local_bits = grid.views[zero_vertex]
    #print(grid.vertex_to_positive_bits.keys())
    zero_bit = positive_time_cells_on_vertex(dimension, vertex = zero_vertex, sign=True , celldim =2)[0]
    coordiantes_of_zero_bit = coordiantes_of_k_faces([zero_bit], dimension)[0]
    print(zero_bit)
    print(coordiantes_of_zero_bit)
    
    #if dimension == 3:
        #cube = [  ((np.int64(0),np.int64(0),np.int64(0)),(np.int64(0),np.int64(1),np.int64(1))), 
                  #((np.int64(0),np.int64(0),np.int64(0)),(np.int64(1),np.int64(0),np.int64(1))),
                  #((np.int64(0),np.int64(0),np.int64(0)),(np.int64(1),np.int64(1),np.int64(0))),
                  #((np.int64(1),np.int64(0),np.int64(0)),(np.int64(1),np.int64(1),np.int64(1))),
                  #((np.int64(0),np.int64(1),np.int64(0)),(np.int64(1),np.int64(1),np.int64(1))),
                  #((np.int64(0),np.int64(0),np.int64(1)),(np.int64(1),np.int64(1),np.int64(1))) ]


    total, miss = 0, 0 

    for binary_assignment in local_gen(local_bits):
        relevant_set = [ ]
        for bit, value in zip(local_bits, binary_assignment):
            temp_assignment[bit] ^= value
            if value == 1:
                relevant_set.append(bit)

        res = grid.correction_cycele_swift_rule(deepcopy(temp_assignment))
        if grid.syndrom_size(res) > 0 and res[zero_bit] == 1:
            total += 1
            faces_subset = [ ] 
            if not span_step( coordiantes_of_zero_bit, coordiantes_of_k_faces(relevant_set, dimension), dimension ):
                miss += 1
                print(False)
                for point in coordiantes_of_k_faces(relevant_set, dimension):
                    print(point)
                print(sum(temp_assignment.values()))
        for bit, value in zip(local_bits, binary_assignment):
            temp_assignment[bit] ^= value
    print()
    print()
    print(float(miss/total))


def check_spanning_growth_toric_edge_verison(dimension):
    grid = KDgrid(4, dimension, celldim=2, checksdim=1)
    temp_assignment = deepcopy(grid.zbits)
    zero_vertex = tuple( 2 for _ in range(dimension) ) # (1,1,1,..)
    #print(grid.vertex_to_positive_bits.keys())
    zero_check = tuple( (zero_vertex, (3,2,2)) )
    u,v = (2,1,2), (2,2,1)

    local_bits = set(grid.views[zero_vertex])
    for w in [u,v]:
        for bit in grid.views[v]:
            local_bits.add(bit) 
    checks = set()
    for bit in local_bits:
        for check in grid.bits_to_checks[bit]:
            checks.add( check  )

    coordiantes_of_zero_check = coordiantes_of_k_faces([zero_check], dimension)[0]
    print(zero_check)
    print(coordiantes_of_zero_check)
    #print(local_bits)
    #exit(0)
    total, miss = 0, 0 
    for binary_assignment in local_gen(local_bits):
        relevant_set = [ ]
        for bit, value in zip(local_bits, binary_assignment):
            temp_assignment[bit] ^= value
            
        for check in checks:
            if grid.local_syndrom(check, temp_assignment) == 1:
                relevant_set.append(check)

        res = grid.correction_cycele_swift_rule(deepcopy(temp_assignment))
        if grid.local_syndrom(zero_check, res) == 1:
            total += 1
            faces_subset = [ ] 
            if not span_step( coordiantes_of_zero_check, coordiantes_of_k_faces(relevant_set, dimension), dimension ):
                miss += 1
                print(False)
                print("".join(str(_) for _ in binary_assignment))
#                for point in coordiantes_of_k_faces(relevant_set, dimension):
#                    print(point)
#                print(sum(temp_assignment.values()))
        for bit, value in zip(local_bits, binary_assignment):
            temp_assignment[bit] ^= value
    print()
    print(total, miss)
    print(float(miss/total))


def plot_vs_digonal():
    grid = KDgrid(10, 2, celldim=2, checksdim=1)
    assign = deepcopy(grid.zbits)
    for _ in range(8):
        z = np.int64(_)
        assign[((z,z),(z+1,z+1))] = 1

    for t in range(400):
        c = canvas.canvas()
        for face in grid.face_to_vertex.keys():
            twoD_grid_projrct_face(face, c)
        if t > 200:
            assign = grid.correction_cycele_swift_rule(assign) 
        for face,val in assign.items():
            twoD_grid_set_bit_on_face( face,val,c)
        c.writeSVGfile(f"canvas_test_digonal_{grid.n}_i{t}")
    system(f"ffmpeg -start_number 1 -i canvas_test_digonal_{grid.n}_i%d.svg -vcodec mpeg4 canvas_test_digonal_{grid.n}.avi")

def single_run(grid, p, decoding, error, time, attempts, attempt_number, verbose = None, accu = None, twoD_plot = False, treeD_plot = False ):
    if verbose:
        print(f"[#] Attempt number: {attempt_number}, p: {p}")
    assign = grid.random_assignment(p, assignment = None)


    for _ in range(time):
        if twoD_plot:
            c = canvas.canvas()
            for face in grid.face_to_vertex.keys():
                twoD_grid_projrct_face(face, c)
        elif treeD_plot:
            c = canvas.canvas()
            for face in grid.face_to_vertex.keys():
                projrct_face(face, c)
        error[_] +=  grid.syndrom_size(assign)  / (len(grid.checks.keys()) * attempts)
        if treeD_plot:
            for edge in grid.get_syndrom(assign):
                set_bit_on_edge(edge ,c)
        assign = decoding(_, assign) 
        if accu:
            assign = grid.random_assignment(p, assignment = assign)
        if verbose: 
            print( f"\t[>] iteration number: {_}" )

        if twoD_plot:
            for face,val in assign.items():
                twoD_grid_set_bit_on_face( face,val,c)
            c.writeSVGfile(f"canvas_test_{grid.n}_i{_}_a{attempt_number}")
        elif treeD_plot:
            for bit in grid.debug_picked:
                set_bit_on_face( bit, 1,c)
            c.writeSVGfile(f"canvas_test_{grid.n}_{grid.k}_i{_}_a{attempt_number}")
    if twoD_plot:
        system(f"ffmpeg -start_number 1 -i canvas_test_{grid.n}_i%d_a{attempt_number}.svg -vcodec mpeg4 canvas_test_{grid.n}_{attempt_number}.avi")
    if treeD_plot:
        system(f"ffmpeg -start_number 1 -i canvas_test_{grid.n}_{grid.k}_i%d_a{attempt_number}.svg -vcodec mpeg4 canvas_test_{grid.n}_{grid.k}_{attempt_number}.avi")

def single_run_count_X_gnes(grid, p, decoding, error, time, attempts, attempt_number, verbose = None, accu = None, histogram=False): 

    if (grid.k != 3) or (grid.celldim != 2) or (grid.checksdim != 1):
        raise Exception('Not 3D toric, checks should be set on the edges') 

    if verbose:
        print(f"[#] Attempt number: {attempt_number}")
    assign = grid.random_assignment(p, assignment = None)
    lost = False
    for _ in range(time):
        if not lost :
            if sum(  check_X_generators(grid, assign ) ) != 0 :
                error[_] +=  1.0 / attempts
                for __ in range(_ + 1, time):
                    if not histogram:
                        error[__] +=  1.0 / attempts
                print('shit')
                lost = True
                break
#        else:
#            error[_] +=  1.0 / attempts
        assign = decoding(_, assign) 
        if accu:
            assign = grid.random_assignment(p, assignment = assign)
        if verbose: 
            print( f"\t[>] iteration number: {_}" )

def TestCase(ns, ks, p_rates, decode_cycele, title, accu = True, attempts = 80, time = 80, verbose=True, celldim=2, checksdim =0, diff = 0, twoD_plot = False, treeD_plot = False, count_X = False, histogram= False):
    plt.clf()
    process = [ ]
    errors = [ ]
    for n,k in zip(ns, ks):
        grid = KDgrid(n,k, celldim=celldim, checksdim=checksdim, diff = diff)
        for p in p_rates:
            process_exp = [ ]
            errors.append( Array('d', [ 0 for _ in range( time ) ] ))
            for __ in range(attempts):
                decoding = {
                    "by_colors" : lambda x,y : grid.correction_cycele(y, color= ( x % 32 ) ),
                    "all_major" : lambda x,y : grid.correction_cycele_all_take_maj(y),
                    "rand_pair" : lambda x,y : grid.correction_cycele_random_pair(y),
                    "max_color" : lambda x,y : grid.correction_cycele_max_color(y),
                    "swift_rul" : lambda x,y : grid.correction_cycele_swift_rule(y),
                    "none" : lambda x,y : y 
                    }[decode_cycele]
                if not count_X:
                    process_exp.append(Process(target = single_run,
                                           args=(grid, p, decoding, errors[-1], time, attempts, __ , verbose , accu, twoD_plot, treeD_plot )))
                else:
                    process_exp.append(Process(target = single_run_count_X_gnes,
                                           args=(grid, p, decoding, errors[-1], time, attempts, __ , verbose , accu, histogram )))

            process.append( process_exp ) 
            for proc in process_exp:
                proc.start()
                proc.join()

    for j, process_exp in enumerate( process ):
#        for proc in  process_exp:
#            proc.join()
        plt.plot(errors[j], label =f'{j}')
    plt.legend()

    plt.title(f"{title} - {decode_cycele}") # fontsize=14, fontweight='bold', loc='center')
    detail = "\n".join( [ 

            f"side-length        :{ns}", 
            f"grid dim           :{ks}", 
            f"error rates        :{ p_rates}", 
            f"error accumulation :{ accu}"
    ])
    plt.text(0.1, 0.1, detail , fontsize=9, transform=plt.gcf().transFigure)
    plt.subplots_adjust(bottom=0.3)
    plt.savefig(f"test_{title}-t:{time}-a:{attempts}-ns:{ns}-p:{p_rates}.svg")

def tests():
    def inital_samll_grid( ):
        grid = KDgrid(5,3)
        print(grid.views[ (0,0,0)][0])
        print()
        print(len(grid.views[ (0,0,0)]))
        print()
        print()
        print(grid.views[ (1,0,0)])
        print()
        print(len(grid.views[ (1,0,0)]))
        print()
        print()
        print(grid.views[ (0,1,0)])
        print()
        print()
        print()
        print(grid.views[ (0,0,1)])

        c = canvas.canvas()
        for face in grid.face_to_vertex.keys():
            projrct_face(face, c)
        c.writeSVGfile("test-3x3")
    
    def twoD_inital_samll_grid( ):
        grid = KDgrid(5,2)
        c = canvas.canvas()
        for face in grid.face_to_vertex.keys():
            twoD_grid_projrct_face(face, c)
        c.writeSVGfile("test-5x5")
    



    def inital_samll_grid_var_cell_dim( ):
        grid = KDgrid(5,3, celldim=2, checksdim = 1)
        print(grid.checks_to_bits[ ( (0,0,0) , (0,0,1) ) ][0])
        print(grid.checks_to_bits[ ( (0,0,0) , (0,0,1) ) ])
    
    def set_bitson_single_face():

        grid = KDgrid(5,3)
        c = canvas.canvas()
        for face in grid.views[(2,1,1)]:
            projrct_face(face, c)
        
        for face in grid.views[(2,1,1)]:
            set_bit_on_face( face,"1",c)

        c.writeSVGfile("test-bits-on-face-5x3")

    def test_random_error():
        grid = KDgrid(4,3)
        assign = grid.random_assignment(0.5, assignment = None) 

        c = canvas.canvas()
        for face in grid.face_to_vertex.keys():
            projrct_face(face, c)

        for face,val in assign.items():
            set_bit_on_face( face,"{0}".format(val),c)
        c.writeSVGfile("random_error")

    def test_colorized_c():
        grid = KDgrid(5,3)
        for color, faces in grid.get_colorized().items():
            c = canvas.canvas()
            for face in faces:
                projrct_face(face, c)
            c.writeSVGfile("test_colorized_c_{0}".format(color))

    def test_correction_cycle():
        grid = KDgrid(5,3)
        assign = grid.random_assignment(0.1, assignment = None) 

        c = canvas.canvas()
        for face in grid.face_to_vertex.keys():
            projrct_face(face, c)

        for face,val in assign.items():
            set_bit_on_face( face,"{0}".format(val),c)

        c.writeSVGfile("random_error_before_correction")
        assign = grid.correction_cycele(assign, color=0)
        for face,val in assign.items():
            set_bit_on_face( face,"{0}".format(val),c)
        c.writeSVGfile("random_error_after_correction")

    def test_correction_cycle_random_pair():
        grid = KDgrid(5,3)
        assign = grid.random_assignment(0.1, assignment = None) 

        c = canvas.canvas()
        for face in grid.face_to_vertex.keys():
            projrct_face(face, c)

        for face,val in assign.items():
            set_bit_on_face( face,"{0}".format(val),c)

        c.writeSVGfile("random_error_before_correction_random_pair")
        assign = grid.correction_cycele_random_pair(assign)
        for face,val in assign.items():
            set_bit_on_face( face,"{0}".format(val),c)
        c.writeSVGfile("random_error_after_correction_random_pair")


    def test_correction():
        TestCase([8, 16], [3, 3], [0.001], "by_colors", "test_correction", accu = False, attempts=1) 
        plt.show()

    def test_correction_random_pair():
        TestCase([8], [3], [0.0001, 0.001], "rand_pair", "test_correction_rand", accu = False)
        #plt.show()

    def test_variable_noise_random_pair():
        TestCase([8], [3], [0.0001,0.001, 0.005, 0.02, 0.05], "rand_pair", "test_variable_noise_random_pair_no_accu", accu = False)
        
    def test_correction_error_accu():
        TestCase([3,4,5,7,8], [3,3,3,3,3], [0.02], "by_colors", "test_correction_error_accu", accu = True)

    def test_correction_error_accu_all_maj():
        TestCase([7, 14, 20, 30], [3,3,3,3], [0.0001], "all_major", "test_correction_error_accu_all_maj", accu = True)

    def test_correction_error_accu_random_pairs():
        TestCase([7, 14, 20, 30], [3,3,3,3,3], [0.0001], "rand_pair", "test_correction_error_accu_random_pairs", accu = True)

    def test_variable_noise_error_accu():
        TestCase([8], [3], [0.0001,0.001, 0.005, 0.02, 0.05], "by_colors", "test_variable_noise_error_accu", accu = True)

    def test_variable_noise_error_accu_random_pairs():
        TestCase([8], [3], [0.0001,0.001, 0.002, 0.004], "rand_pair", "test_variable_noise_error_accu_random_pairs", accu = True)

    def test_correction_error_accu_low_noise():
        TestCase([5, 10], [3,3], [0.00001], "by_colors", "test_correction_error_accu_low_noise", accu = True, times = 500, attempts = 100)


    def test_all_the_decoders_no_accu( ):
#        TestCase([8], [3], [0.001], "by_colors", "test_correction_colors_1", accu = False) 
#        TestCase([8], [3], [0.001], "all_major", "test_correction_all__1", accu = False)
#        TestCase([8], [3], [0.0001], "rand_pair", "test_correction_rand_1", accu = False)
        TestCase([8, 16, 20, 30], [3, 3, 3, 3], [0.001], "by_colors", "test_correction_colors_2", accu = False, attempts=1, time = 50)
        TestCase([8, 16, 20, 30], [3, 3, 3, 3], [0.001], "all_major", "test_correction_all__2", accu = False,  attempts=1, time = 50)
        TestCase([8, 16, 20, 30], [3, 3, 3, 3], [0.001], "rand_pair", "test_correction_rand_2", accu = False, attempts=1, time = 50)
        #plt.show()

    def test_rand_pair_many_30_no_accu( ):
        TestCase([8, 16, 20, 30, 30, 30, 30], [3, 3, 3, 3, 3, 3, 3], [0.001], "rand_pair", "test_correction_rand_2_8-20_30x4", accu = False, attempts=1, time = 500)

    def test_by_rand_pair_many_30_plus_accu_countX( ):
        p =[0.001]
        TestCase([8,10,12,14,16,18], [3, 3, 3, 3, 3, 3, 3], p, "rand_pair", f"test_correction_rand_2_8-20_30x4_plus_accu_countX", accu = True, attempts=100, time = 100, checksdim=1, count_X = True)

    def test_all_major_many_30_no_accu( ):
        TestCase([8, 16, 20, 30, 30, 30, 30], [3, 3, 3, 3, 3, 3, 3], [0.01], "all_major", "test_correction_all_major_2_8-20_30x4_p0.01", accu = False, attempts=1, time = 500)
    def test_all_major_many_30_plus_accu( ):
        TestCase([8, 16, 20, 30, 30, 30, 30], [3, 3, 3, 3, 3, 3, 3], [0.001], "all_major", "test_correction_accu_all_major_2_8-20_30x4", accu = True, attempts=1, time = 500)
    def test_all_major_many_30_plus_accu_diff_changed( ):
        TestCase([8, 16, 20, 30, 30, 30, 30], [3, 3, 3, 3, 3, 3, 3], [0.001], "all_major", "test_correction_all_major_change_diff-2_accu_2_8-20_30x4", accu = True, attempts=1, time = 1000, diff = -2)
    def test_all_major_many_30_plus_accu_diff_changed_vp( ):
        TestCase([8, 16, 20, 30, 30, 30, 30], [3, 3, 3, 3, 3, 3, 3], [0.0005], "all_major", "test_correction_all_major_change_diff-2_lower_noise_accu_2_8-20_30x4", accu = True, attempts=1, time = 1000, diff = -2)
    def test_all_major_many_30_plus_accu_diff_changed_high_p( ):
        TestCase([8, 16, 20, 30, 30, 30, 30], [3, 3, 3, 3, 3, 3, 3], [0.01], "all_major", "test_correction_all_major_change_diff-2_high_noise_accu_2_8-20_30x4", accu = True, attempts=1, time = 1000, diff = -2)
    def test_by_colors_many_30_no_accu( ):
        TestCase([8, 16, 20, 30, 30, 30, 30], [3, 3, 3, 3, 3, 3, 3], [0.001], "by_colors", "test_correction_by_colors_2_8-20_30x4", accu = False, attempts=1, time = 500)

    def test_by_colors_many_30_plus_accu( ):
        TestCase([8, 16, 20, 30, 30, 30, 30], [3, 3, 3, 3, 3, 3, 3], [0.001], "by_colors", "test_correction_accu_by_colors_2_8-20_30x4", accu = True, attempts=1, time = 500)

    def test_by_max_color_many_30_no_accu( ):
        TestCase([8, 16, 20, 30, 30, 30, 30], [3, 3, 3, 3, 3, 3, 3], [0.001], "max_color", "test_correction_by_MAX_2_8-20_30x4", accu = False, attempts=1, time = 200)
    def test_by_max_color_many_30_no_accu_diff_change( ):
        TestCase([8, 16, 20, 30, 30, 30, 30], [3, 3, 3, 3, 3, 3, 3], [0.001], "max_color", "test_correction_by_MAX_changed_diff-2_2_8-20_30x4", accu = False, attempts=1, time = 200, diff=-2)
    def test_by_max_color_many_30_plus_accu_diff_change( ):
        TestCase([8, 16, 20, 30, 30, 30, 30], [3, 3, 3, 3, 3, 3, 3], [0.001], "max_color", "remote_correction_accu_by_MAX_changed_diff-2_2_8-20_30x4", accu = True, attempts=1, time = 200, diff=-2)
    def test_by_max_color_many_30_plus_accu( ):
        TestCase([8, 16, 20, 30, 30, 30, 30], [3, 3, 3, 3, 3, 3, 3], [0.001], "max_color", "remote_correction_accu_by_MAX_2_8-20_30x4", accu = True, attempts=1, time = 500)
    def test_by_swift_rule_many_30_no_accu( ):
        TestCase([8, 16, 20, 30, 30, 30, 30], [3, 3, 3, 3, 3, 3, 3], [0.02], "swift_rul", "test_correction_by_SWIFT_2_8-20_30x4", accu = False, attempts=1, time = 200)

    def test_by_swift_rule_many_30_plus_accu( ):
        p =[0.01]
        TestCase([8, 16, 30], [3, 3, 3, 3, 3, 3, 3], p, "swift_rul", f"test_correction_by_SWIFT_2_8-20_30x4_plus_accu_{p[0]}", accu = True, attempts=1, time = 100, checksdim=1)

    def test_by_swift_rule_many_30_plus_accu_countX( ):
        p =[0.001]
        TestCase([8, 10, 12], [3, 3, 3, 3, 3, 3, 3], p, "swift_rul", f"test_correction_by_SWIFT_2_8-20_30x4_plus_accu_countX", accu = True, attempts=100, time = 100, checksdim=1, count_X = True)

    def test_by_majority_many_30_plus_accu_countX( ):
        p =[0.0035]
        TestCase([8, 14], [3, 3, 3, 3, 3, 3, 3], p, "all_major", f"test_correction_by_all_major_2_8-20_30x4_plus_accu_countX", accu = True, attempts=1000, time = 40, checksdim=1, count_X = True)

    def test_by_swift_rule_many_30_canvas( ):
        TestCase([16], [3, 3, 3, 3, 3, 3, 3], [0.05], "swift_rul", "test_correction_by_SWIFT_2_8-20_30x4_canvas", accu = False, attempts=1, time = 40, treeD_plot=True, checksdim = 1 )
    def test_by_swift_rule_many_30_plus_accu_canvas( ):
        TestCase([30], [3, 3, 3, 3, 3, 3, 3], [0.001], "swift_rul", "test_correction_by_SWIFT_2_8-20_30x4_canvas", accu = True, attempts=1, time = 40, treeD_plot=True, checksdim = 1 )
    def test_classic_by_tooms_rule_many_30_plus_accu( ):
        TestCase([10, 100, 200] , [2, 2, 2, 2, 2, 2, 2] , [0.01], "swift_rul", "test_classic_by_tooms_rule_many_30_plus_accu", accu = True, attempts=25, time = 20, celldim=2, checksdim =1)
    def test_classic_by_tooms_rule_many_30_canvas( ):
        TestCase([20] , [2, 2, 2, 2, 2, 2, 2] , [0.3], "swift_rul", "test_classic_by_tooms_rule_many_30", accu = False, attempts=1, time = 100, celldim=2, checksdim =1, twoD_plot = True)
    def test_classic_by_tooms_rule_many_30_plus_accu_canvas( ):
        TestCase([100] , [2, 2, 2, 2, 2, 2, 2] , [0.05], "swift_rul", "test_classic_by_tooms_rule_many_30_plus_accu", accu = True, attempts=1, time = 100, celldim=2, checksdim =1, twoD_plot = True)
    def test_by_swift_rule_many_50_plus_accu( ):
        TestCase([8, 16, 50], [3, 3, 3, 3, 3, 3, 3], [0.001], "swift_rul", "test_correction_by_SWIFT_2_8-16-100_plus_accu", accu = True, attempts=1, time = 200 )
    def test_no_decoding_case( ):
        TestCase([8, 16, 30, 30, 30, 30, 30], [3, 3, 3, 3, 3, 3, 3], [0.001], "none", "test_correction_by_None_2_8-20_30x4_plus_accu", accu = True, attempts=1, time = 200)


    def test_by_swift_rule_small_size_8_no_accu( ):
        TestCase([8], [3, 3, 3, 3, 3, 3, 3], [0.02], "swift_rul", "test_correction_by_SWIFT_2_5x7", accu = False, attempts=1, time = 10, verbose=True)
    def test_4D_toric_sanity():
        #TestCase([8], [3], [0.001], "by_colors", "test_correction_colors_1", accu = False) 
        TestCase([8], [4], [0.001], "all_major", "test_4D_toric_sanity", accu = False, celldim = 2 , checksdim= 1 )
        #TestCase([8], [3], [0.0001], "rand_pair", "test_correction_rand_1", accu = False)

    def test_4D_toric_no_accu():
        TestCase([8, 16, 20], [4, 4, 4], [0.0001], "by_colors", "test_4D_correction_colors_2", accu = False, celldim = 2 , checksdim= 1) 
        TestCase([8, 16, 20], [4, 4, 4], [0.0001], "all_major", "test_4D_correction_all__2", accu = False, celldim = 2 , checksdim= 1)
        TestCase([8, 16, 20], [4, 4, 4], [0.0001], "rand_pair", "test_4D_correction_rand_2", accu = False, celldim = 2 , checksdim= 1)
    def test_4D_toric_no_accu_single_attempt():
        TestCase([8, 16, 20, 20, 20, 20, 20], [4, 4, 4, 4, 4, 4], [0.001], "by_colors", "test_4D_correction_colors_2_single", accu = False, celldim = 2 , checksdim= 1, attempts=1) 
        TestCase([8, 16, 20, 20, 20, 20, 20], [4, 4, 4, 4, 4, 4], [0.001], "all_major", "test_4D_correction_all__2_single", accu = False, celldim = 2 , checksdim= 1, attempts=1)
        TestCase([8, 16, 20, 20, 20, 20 ,20], [4, 4, 4, 4, 4, 4], [0.001], "rand_pair", "test_4D_correction_rand_2_single", accu = False, celldim = 2 , checksdim= 1, attempts=1)
    #inital_samll_grid()
    #set_bitson_single_face()
    #test_random_error()
    #test_colorized_c()
    #test_correction_cycle()
    #test_correction_cycle_random_pair()
    #test_correction()
    #test_correction_error_accu_random_pairs()
    #test_variable_noise_error_accu_random_pairs()
    #test_correction_error_accu_low_noise()

    #test_correction_error_accu_all_maj()
    #test_correction_random_pair()
    #test_variable_noise_random_pair()
    #test_correction_error_accu_random_pairs()

    #test_all_the_decoders_no_accu()
    #test_rand_pair_many_30_no_accu()
    #test_all_major_many_30_no_accu()
#    test_all_major_many_30_plus_accu()
#    test_by_colors_many_30_plus_accu()
    #inital_samll_grid_var_cell_dim()
    #test_4D_toric_sanity()
    #test_4D_toric_no_accu()

    #test_by_max_color_many_30_plus_accu()
    #test_4D_toric_no_accu_single_attempt()
    #test_by_swift_rule_small_size_8_no_accu()
    #test_correction( )
    #test_by_max_color_many_30_plus_accu()
    #test_all_major_many_30_plus_accu_diff_changed_vp()
    #test_all_major_many_30_plus_accu_diff_changed_high_p()
    #test_by_max_color_many_30_no_accu_diff_change()
    #test_by_max_color_many_30_plus_accu_diff_change()
    #test_by_swift_rule_many_30_no_accu()
    #test_by_swift_rule_many_50_plus_accu()
    #test_by_swift_rule_many_30_plus_accu()
    #test_by_swift_rule_small_size_8_no_accu()
    #test_no_decoding_case()
    #test_classic_by_tooms_rule_many_30_canvas()
    #test_classic_by_tooms_rule_many_30_plus_accu_canvas()
    #twoD_inital_samll_grid()
    #test_by_swift_rule_many_30_canvas()

    #test_by_rand_pair_many_30_plus_accu_countX()
    #test_by_majority_many_30_plus_accu_countX()
    #test_by_swift_rule_many_30_plus_accu_countX()
    #test_by_swift_rule_many_30_plus_accu_canvas()

    #correlation_test()
    #check_spanning_growth_toric(2)
    #check_spanning_growth_toric(3)
    #check_spanning_growth_toric(4)
    #load_pkl()
    #plot_vs_digonal()
    check_spanning_growth_toric_edge_verison(3)

if __name__ == "__main__" :
    tests()
    system('rm canvas_test_*')
