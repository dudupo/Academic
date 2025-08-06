
from pyx import *
import numpy as np
from itertools import combinations, product
from copy import deepcopy
from random import random, shuffle, choice
import matplotlib.pyplot as plt

def _direct(i,k):
    ret = np.zeros(k, dtype=int)
    ret[i] = 1
    return ret

def directions_vec(k):
    return [ _direct(i, k)  for i in range(k) ]

def faces_vec(k, vertex = None, sign=True):

    def totuple( vec ):
        return tuple( i for i in vec ) 

    directions = directions_vec(k)
    vertex = np.zeros(k, dtype=int) if vertex == None else  np.array(vertex, dtype=int)
    ret = [ ]
    for i in range(k-1):
        for j in range(i+1,k):
            signs = product([-1,1], repeat=2) if sign else [  (1,1) ]
            for sign_i, sign_j in signs:
                left, right = deepcopy(vertex), deepcopy(vertex)
                if sign_i == -1:
                    left  -= directions[i]
                else:
                    right += directions[i]
                if sign_j == -1:
                    left  -= directions[j]
                else:
                    right += directions[j]
                ret += [ ( totuple(left), totuple(right) ) ] 
    return ret


class KDgrid:
    def __init__(self, n, k):
        self.n, self.k = n, k
        self.vertices = list( product(range(n), repeat=k) )
     
        self.face_to_vertex = { }
        self.zbits = { } 

        for u in list( product(range(n), repeat=k) ):
            for face in self.faces_vec(vertex=u, sign=False):
                _face = tuple(self.on_the_grid(face, req_depth=2))
                self.zbits[_face] = 0 

        self.views = { }
        for u in list( product(range(n), repeat=k) ):
            self.views[u] = [ ]
            for face in self.faces_vec(vertex=u, sign=True):
                _face = tuple(self.on_the_grid(face, req_depth=2))
                self.views[u].append(_face) 
                if _face not in self.face_to_vertex:
                    self.face_to_vertex[_face] = []
                self.face_to_vertex[_face].append( self.on_the_grid(u, req_depth=1)  )

        self.colorized_dic = self.get_colorized()

    def _direct(self, i):
        return _direct(i, self.k)

    def directions_vec(self):
        return directions_vec(self.k)

    def faces_vec(self, vertex = None, sign=True):
        return faces_vec(self.k, vertex = vertex, sign=sign)
    
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
            return { key : f() for key in self.get_zerobits().keys() }
        else:
            for key,val in assignment.items():
                assignment[key] ^= f()
            return assignment
            #return { key : f() ^ assignment[key] for key in self.get_zerobits().keys() }

    def local_correaction(self, face, assignment):
        stabilizers = self.face_to_vertex[face]
        syndrom_diff = 0
        for stabilizer in stabilizers:
            bits = self.views[stabilizer]
            parity = 0 
            for bit in bits:
                parity ^= assignment[bit]
            syndrom_diff += { 0 : 1 , 1 : -1}[parity]
        if syndrom_diff < 0:
            return True

    def local_correaction_group(self, faces, assignment):
        flipped = { face : False for face in faces  }
        for face in faces:
            flipped[face] = self.local_correaction(face, assignment)
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
            for stabilizer in self.face_to_vertex[face]:
                for facej in self.views[stabilizer]:
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

def project2D(point):
    x,y,z = point
    _x, _y = x + 0.2*y, z + 0.3*y
    return 5*_x, 5*_y
def projrct_face(face, canvas):
    x,y = face
    ax,bx,cx = x
    ay,by,cy = y
    if ax == ay:
        A = (ax,bx,cx)
        B = (ax,by,cx)
        C = (ax,by,cy)
        D = (ax,bx,cy)
    elif bx == by:
        A = (ax,bx,cx)
        B = (ay,bx,cx)
        C = (ay,bx,cy)
        D = (ax,bx,cy)
    else:
        A = (ax,bx,cx)
        B = (ay,bx,cx)
        C = (ay,by,cx)
        D = (ax,by,cx)
    #else:
     #   return
    _A,_B,_C,_D = (project2D(I) for I in [A,B,C,D])

    def stroke_path(x0,y0,x1, y1, canvas):
        if (abs(x0 - x1) > 5) or (abs(y0 - y1) > 5) :
            if abs(x0 - x1) > 5:
                canvas.stroke(path.curve(x0,y0, 0.33 *x0 +0.66*x1 , 0.33 *y0+ 0.66*y1 + 1.2 , 0.66 *x0+ 0.33*x1,0.66 *y0+0.33*y1 + 1.2,  x1,y1), [style.linewidth(0.05), color.rgb.blue] )
            else:
                canvas.stroke(path.curve(x0,y0, 0.33 *x0 +0.66*x1 + 1.2 , 0.33 *y0+ 0.66*y1  , 0.66 *x0+ 0.33*x1 + 1.2,0.66 *y0+0.33*y1 ,  x1,y1), [style.linewidth(0.05), color.rgb.green])
        else:
            canvas.stroke(path.line(x0,y0, x1,y1), [style.linewidth(0.05)])

    stroke_path(*_A, *_B ,canvas)
    stroke_path( *_B, *_C,canvas)
    stroke_path( *_C, *_D,canvas)
    stroke_path( *_D, *_A,canvas)

def set_bit_on_face(face, _text , canvas):
    u,v = face
    u,v = project2D(u), project2D(v)
    z = 0.5*u[0] + 0.5*v[0], 0.5*u[1] + 0.5*v[1]
    canvas.text(z[0], z[1], _text, [text.halign.boxcenter, text.size.normalsize, color.rgb.red])
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

    def test_correction():
        grid = KDgrid(8,3)
        
        attempts = 80
        time = 200

        error = [ 0 for _ in range(time) ]
        for __ in range(attempts):
            print(__)
            assign = grid.random_assignment(0.02, assignment = None) 
            for _ in range(time):
                error[_] +=  (sum(assign.values())/len(grid.zbits))/attempts  
                assign = grid.correction_cycele(assign, color= ( _ % 32 ) )
        plt.plot(error)
        plt.show()
        
    def test_correction_error_accu():
        for n in [3,4,5,7,8]:
            grid = KDgrid(n,3)
            
            attempts = 80
            time = 80

            error = [ 0 for _ in range(time) ]
            for __ in range(attempts):
                print(__)
                assign = grid.random_assignment(0.02, assignment = None) 
                for _ in range(time):
                    error[_] +=  (sum(assign.values())/len(grid.zbits))/attempts  
                    assign = grid.correction_cycele(assign, color= ( _ % 32 ) )
                    assign = grid.random_assignment(0.02, assignment = assign) 
            plt.plot(error)
        plt.show()
    def test_variable_noise_error_accu():
        for p in [0.0001,0.001, 0.005, 0.02, 0.05]:
            grid = KDgrid(8,3)
            
            attempts = 80
            time = 80

            error = [ 0 for _ in range(time) ]
            for __ in range(attempts):
                print(__)
                assign = grid.random_assignment(p, assignment = None) 
                for _ in range(time):
                    error[_] +=  (sum(assign.values())/len(grid.zbits))/attempts  
                    assign = grid.correction_cycele(assign, color= ( _ % 32 ) )
                    assign = grid.random_assignment(p, assignment = assign) 
            plt.plot(error)
        plt.show()
    def test_correction_error_accu_low_noise():
        for n in [5, 10]:
            
            attempts = 100
            time = 500

            error = [ 0 for _ in range(time) ]
            for __ in range(attempts):
                grid = KDgrid(n,3)
                print(__)
                assign = grid.random_assignment(0.00001, assignment = None) 
                for _ in range(time):
                    error[_] +=  (sum(assign.values())/len(grid.zbits))/attempts  
                    assign = grid.correction_cycele(assign, color= ( _ % 32 ) )
                    assign = grid.random_assignment(0.00001, assignment = assign) 
            plt.plot(error)
        plt.show()
    #inital_samll_grid()
    #set_bitson_single_face()
    #test_random_error()
    #test_colorized_c()
    #test_correction_cycle()
    #test_correction()
    #test_correction_error_accu()
    #test_variable_noise_error_accu()
    test_correction_error_accu_low_noise()

if __name__ == "__main__" :
    tests()
