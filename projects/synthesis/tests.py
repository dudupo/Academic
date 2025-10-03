

from pyx import *
import numpy as np
from itertools import combinations, product
from copy import deepcopy
from random import random, shuffle, choice
import matplotlib.pyplot as plt

from complex import *
from colorize_grids import *

def TestCase(ns, ks, p_rates, decode_cycele, title, accu = True, attempts = 80, time = 80, verbose=True, celldim=2, checksdim =0):
    plt.clf()
    for n,k in zip(ns, ks):
        grid = KDgrid(n,k, celldim=celldim, checksdim=checksdim)
        for p in p_rates:
            error = [ 0 for _ in range(time) ]
            for __ in range(attempts):
                if verbose:
                    print(f"[#] Attempt number: {__}")
                assign = grid.random_assignment(p, assignment = None)
                for _ in range(time):
                    error[_] +=  grid.syndrom_size(assign) / (len(grid.checks.keys()) * attempts)
                    assign =  {
                        "by_colors" : grid.correction_cycele(assign, color= ( _ % 32 ) ),
                        "all_major" : grid.correction_cycele_all_take_maj(assign),
                        "rand_pair" : grid.correction_cycele_random_pair(assign),
                        "max_color" : grid.correction_cycele_max_color(assign),
                        "swift_rul" : grid.correction_cycele_swift_rule(assign)
                    }[decode_cycele]
                    if accu:
                        assign = grid.random_assignment(p, assignment = assign)
            plt.plot(error)

        plt.title(f"{title} - {decode_cycele}") # fontsize=14, fontweight='bold', loc='center')
        detail = "\n".join( [ 

                f"side-length        :{ns}", 
                f"grid dim           :{ks}", 
                f"error rates        :{ p_rates}", 
                f"error accumulation :{ accu}"
        ])
        plt.text(0.1, 0.1, detail , fontsize=9, transform=plt.gcf().transFigure)
        plt.subplots_adjust(bottom=0.3)
        plt.savefig(f"test_{title}.svg")

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
        TestCase([8], [3], [0.02], "by_colors", "test_correction", accu = False) 
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

    def test_all_major_many_30_no_accu( ):
        TestCase([8, 16, 20, 30, 30, 30, 30], [3, 3, 3, 3, 3, 3, 3], [0.001], "all_major", "test_correction_all_major_2_8-20_30x4", accu = False, attempts=1, time = 500)
    def test_by_colors_many_30_no_accu( ):
        TestCase([8, 16, 20, 30, 30, 30, 30], [3, 3, 3, 3, 3, 3, 3], [0.001], "by_colors", "test_correction_by_colors_2_8-20_30x4", accu = False, attempts=1, time = 500)


    def test_by_max_color_many_30_no_accu( ):
        TestCase([8, 16, 20, 30, 30, 30, 30], [3, 3, 3, 3, 3, 3, 3], [0.001], "max_color", "test_correction_by_MAX_2_8-20_30x4", accu = False, attempts=1, time = 200)
    def test_by_swift_rule_many_30_no_accu( ):
        TestCase([8, 16, 20, 30, 30, 30, 30], [3, 3, 3, 3, 3, 3, 3], [0.001], "swift_rul", "test_correction_by_SWIFT_2_8-20_30x4", accu = False, attempts=1, time = 200)

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
    #test_by_colors_many_30_no_accu()
    #inital_samll_grid_var_cell_dim()
    #test_4D_toric_sanity()
    #test_4D_toric_no_accu()

    #test_by_max_color_many_30_no_accu()
    #test_4D_toric_no_accu_single_attempt()
    test_by_swift_rule_many_30_no_accu()
if __name__ == "__main__" :
    tests()
