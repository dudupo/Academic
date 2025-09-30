
from pyx import *
import numpy as np
from itertools import combinations, product
from copy import deepcopy
from random import random, shuffle, choice
import matplotlib.pyplot as plt

from complex import *


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
