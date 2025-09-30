

from pyx import *
import numpy as np
from itertools import combinations, product
from copy import deepcopy
from random import random, shuffle, choice
import matplotlib.pyplot as plt

from complex import *
from colorize_grids import *

def TestCase(ns, ks, p_rates, decode_cycele, title, accu = True, attempts = 80, time = 80, verbose=True):
    plt.clf()
    for n,k in zip(ns, ks):
        grid = KDgrid(n,k)
        for p in p_rates:
            error = [ 0 for _ in range(time) ]
            for __ in range(attempts):
                if verbose:
                    print(f"[#] Attempt number: {__}")
                assign = grid.random_assignment(p, assignment = None)
                for _ in range(time):
                    error[_] +=  (sum(assign.values())/len(grid.zbits))/attempts
                    assign =  {
                        "by_colors" : grid.correction_cycele(assign, color= ( _ % 32 ) ),
                        "all_major" : grid.correction_cycele_all_take_maj(assign),
                        "rand_pair" : grid.correction_cycele_random_pair(assign)
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
        plt.text(0.02, 0.5, detail , fontsize=14, transform=plt.gcf().transFigure)
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
        TestCase([8], [3], [0.02], "rand_pair", "test_correction_rand", accu = False)
        plt.show()

    def test_variable_noise_random_pair():
        TestCase([8], [3], [0.0001,0.001, 0.005, 0.02, 0.05], "rand_pair", "test_variable_noise_random_pair_no_accu", accu = False)
        
    def test_correction_error_accu():
        TestCase([3,4,5,7,8], [3,3,3,3,3], [0.02], "by_colors", "test_correction_error_accu", accu = True)

    def test_correction_error_accu_all_maj():
        TestCase([8], [3], [0.0005, 0.005, 0.05], "all_major", "test_correction_error_accu_all_maj", accu = True)

    def test_correction_error_accu_random_pairs():
        TestCase([7, 14, 20, 30], [3,3,3,3,3], [0.0001], "rand_pair", "test_correction_error_accu_random_pairs", accu = True)

    def test_variable_noise_error_accu():
        TestCase([8], [3], [0.0001,0.001, 0.005, 0.02, 0.05], "by_colors", "test_variable_noise_error_accu", accu = True)

    def test_variable_noise_error_accu_random_pairs():
        TestCase([8], [3], [0.0001,0.001, 0.002, 0.004], "rand_pair", "test_variable_noise_error_accu_random_pairs", accu = True)

    def test_correction_error_accu_low_noise():
        TestCase([5, 10], [3,3], [0.00001], "by_colors", "test_correction_error_accu_low_noise", accu = True, times = 500, attempts = 100)

    #inital_samll_grid()
    #set_bitson_single_face()
    #test_random_error()
    #test_colorized_c()
    #test_correction_cycle()
    #test_correction_cycle_random_pair()
    test_correction()
    #test_correction_random_pair()
    #test_variable_noise_random_pair()
    #test_correction_error_accu_random_pairs()
    #test_variable_noise_error_accu_random_pairs()
    #test_correction_error_accu_random_pairs()
    #test_correction_error_accu_low_noise()
    #test_correction_error_accu_all_maj()


if __name__ == "__main__" :
    tests()
