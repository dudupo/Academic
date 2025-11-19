
from pyx import *
import numpy as np
from itertools import combinations, product
from copy import deepcopy
from random import random, shuffle, choice
import matplotlib.pyplot as plt

from complex import *


def twoD_grid_project2D(point):
    x,y = point
    return 1*x, 1*y

def twoD_grid_projrct_face(face, canvas):
    x,y = face
    ax,bx = x
    ay,by = y
    A = (ax, bx)
    B = (ay, bx)
    C = (ay, by)
    D = (ax, by)
    #else:
     #   return
    _A,_B,_C,_D = (twoD_grid_project2D(I) for I in [A,B,C,D])

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


def twoD_grid_set_bit_on_face(face, _text , canvas):
    if _text == 1:
        u,v = face
        u,v = twoD_grid_project2D(u), twoD_grid_project2D(v)
        rect = path.rect(u[0], u[1], 1, 1)

        # Fill the rectangle with the given color
        canvas.fill(rect, [color.rgb.red])
    #z = 0.5*u[0] + 0.5*v[0], 0.5*u[1] + 0.5*v[1]
    #canvas.text(z[0], z[1], _text, [text.halign.boxcenter, text.size.normalsize, color.rgb.red])

def project2D(point):
    x,y,z = point
    _x, _y = x + 0.2*y, z + 0.3*y
    return 5*_x, 5*_y

def stroke_path(x0,y0,x1, y1, canvas, _color=None):
   
    if (abs(x0 - x1) > 5) or (abs(y0 - y1) > 5) :
        if abs(x0 - x1) > 5:
            _color = [style.linewidth(0.05),color.rgb.blue] if _color is None else _color
            return (path.curve(x0,y0, 0.33 *x0 +0.66*x1 , 0.33 *y0+ 0.66*y1 + 1.2 , 0.66 *x0+ 0.33*x1,0.66 *y0+0.33*y1 + 1.2,  x1,y1),  _color )
        else:
            _color = [style.linewidth(0.05),color.rgb.green] if _color is None else _color
            return (path.curve(x0,y0, 0.33 *x0 +0.66*x1 + 1.2 , 0.33 *y0+ 0.66*y1  , 0.66 *x0+ 0.33*x1 + 1.2,0.66 *y0+0.33*y1 ,  x1,y1),  _color)
    else:
        _color = [style.linewidth(0.05),color.rgb.black] if _color is None else _color
        return (path.line(x0,y0, x1,y1),  _color)
def projrct_face(face, canvas, stroke=True):
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

    if stroke:
        for X,Y in [(_A,_B), (_B,_C), (_C,_D), (_D,_A)]:
            canvas.stroke(*stroke_path(*X, *Y ,canvas))
    else:
        _path, _ = stroke_path( *_A, *_B,canvas)
        for X,Y in [(_B,_C), (_C,_D), (_D,_A) ]:
            p, _ = stroke_path( *X, *Y,canvas)
            _path = _path << p
        #_path.append(path.closepath() )
        canvas.fill( _path, [ color.cmyk.Yellow])

def set_bit_on_face(face, _text , canvas):
    if _text == 1:
        projrct_face(face, canvas, stroke=False)

def set_bit_on_edge(edge, canvas):
    x,y = edge
    x,y = ( project2D(I) for I in (x,y) )
    canvas.stroke(*stroke_path(*x, *y ,canvas, _color=[style.linewidth(0.5),color.rgb.red]))
    
    #u,v = face
    #u,v = project2D(u), project2D(v)
    #z = 0.5*u[0] + 0.5*v[0], 0.5*u[1] + 0.5*v[1]
    #canvas.text(z[0], z[1], _text, [text.halign.boxcenter, text.size.normalsize, color.rgb.red])
