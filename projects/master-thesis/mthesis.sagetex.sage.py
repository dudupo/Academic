## -*- encoding: utf-8 -*-


# This file was *autogenerated* from the file mthesis.sagetex.sage
from sage.all_cmdline import *   # import sage library

_sage_const_1 = Integer(1); _sage_const_0 = Integer(0); _sage_const_17 = Integer(17); _sage_const_2 = Integer(2); _sage_const_3000 = Integer(3000); _sage_const_0p3 = RealNumber('0.3'); _sage_const_9 = Integer(9); _sage_const_7 = Integer(7); _sage_const_3 = Integer(3); _sage_const_4 = Integer(4); _sage_const_5 = Integer(5); _sage_const_6 = Integer(6); _sage_const_8 = Integer(8); _sage_const_13 = Integer(13); _sage_const_14 = Integer(14); _sage_const_10 = Integer(10); _sage_const_11 = Integer(11); _sage_const_12 = Integer(12); _sage_const_15 = Integer(15); _sage_const_83 = Integer(83); _sage_const_63 = Integer(63); _sage_const_0p005 = RealNumber('0.005'); _sage_const_0p01 = RealNumber('0.01'); _sage_const_30 = Integer(30); _sage_const_98 = Integer(98); _sage_const_104 = Integer(104); _sage_const_107 = Integer(107); _sage_const_140 = Integer(140)## This file (mthesis.sagetex.sage) was *autogenerated* from mthesis.tex with sagetex.sty version 2021/10/16 v3.6.
import sagetex
_st_ = sagetex.SageTeXProcessor('mthesis', version='2021/10/16 v3.6', version_check=True)
_st_.current_tex_line = _sage_const_1 
_st_.blockbegin()
try:
 from math import fmod
 from numpy import linspace
 
 #def res(X):
 #  Y = [(X[0][0], X[0][1])]
 #  for x,y in X[1:]:
 #    midx = (Y[-1][0] + x)/2
 #    midy = (Y[-1][1] + y)/2
 #    Y.append( (midx, midy) )
 #    Y.append((x,y))
 #  return Y
 
 def split_lines(X):
   ret = [ [ (X[_sage_const_0 ][_sage_const_0 ], X[_sage_const_0 ][_sage_const_1 ])  ] ]
   for x,y in X[_sage_const_1 :]:
     if abs(y - ret[-_sage_const_1 ][-_sage_const_1 ][_sage_const_1 ]) > _sage_const_1 :
         ret[-_sage_const_1 ].append((x,_sage_const_17 ))
         ret +=  [ [ (x,y) ] ]
     else:
         ret[-_sage_const_1 ].append( (x,y) )
   return ret
 
 def colorgen():
   colors_list = ['gray', 'black']
   i = -_sage_const_1 
   while True:
       i=  mod(i + _sage_const_1 , len(colors_list))
       yield colors_list[ i ]
 _colorgen = colorgen()
 
 def finate_poly_plot(fun, end=_sage_const_17 ):
   _color = next(_colorgen)
   point_lists =  split_lines([ (y, fmod(fun(y),end)) for y in linspace(_sage_const_0 ,end+_sage_const_2 ,_sage_const_3000 ) ])
   pplot_lines =  line(point_lists[_sage_const_0 ], color=_color, aspect_ratio=_sage_const_0p3 )
   for _point_list in point_lists[_sage_const_1 :]:
     pplot_lines += line(_point_list, color=_color, aspect_ratio=_sage_const_0p3 )
   return pplot_lines
 
 #p_list =  split_lines([ (y, fmod(f(y),17)) for y in linspace(0,17,1000) ])
 #pplot_t =  line(p_list[0])
 #for l in p_list[1:]:
 #  pplot_t += line(l)
 #p_list2 = [ (y, fmod(g(y),17)) for y in linspace(0,17,100) ]
 #
 def print_capt(_str):
   return "\caption{The plot " + _str+  " presents the extension of the polynomials}"
 
 def tanner_graph(graph, code):
   for i,edge in enumerate(graph.edges()):
     graph.set_edge_label(*edge[:_sage_const_2 ], f'{code[i]}')
   return graph
 
 def peter_premu(x):
     premu = [_sage_const_1 ,_sage_const_9 ,_sage_const_7 ,_sage_const_0 ,_sage_const_2 ,_sage_const_3 ,_sage_const_4 ,_sage_const_5 ,_sage_const_6 ,_sage_const_8 ,_sage_const_13 ,_sage_const_14 ,_sage_const_10 ,_sage_const_11 ,_sage_const_12 ]
     premuinv = [ _sage_const_0  for _ in range(_sage_const_15 ) ]
     for i in range(_sage_const_15 ):
         for j in range(_sage_const_15 ):
             if premu[j] == i:
                 premuinv[i] = j
     return [ x[premuinv[i]] for i in range(_sage_const_15 ) ]
 
 def peter_graph(code = [_sage_const_0 ,_sage_const_1 ,_sage_const_1 ,_sage_const_0 ,_sage_const_0 ,_sage_const_1 ,_sage_const_1 ,_sage_const_0 ,_sage_const_1 ,_sage_const_1 ,_sage_const_0 ,_sage_const_1 ,_sage_const_0 ,_sage_const_0 ,_sage_const_1 ]):
   #code = list(range(15)) #[0,1,1,0,0,1,1,0,1,1,0,1,0,0,1]
   peter = graphs.PetersenGraph()
   return tanner_graph(peter, code)
 
 def peter_graphs():
     code = [_sage_const_0 ,_sage_const_1 ,_sage_const_1 ,_sage_const_0 ,_sage_const_0 ,_sage_const_1 ,_sage_const_1 ,_sage_const_0 ,_sage_const_1 ,_sage_const_1 ,_sage_const_0 ,_sage_const_1 ,_sage_const_0 ,_sage_const_0 ,_sage_const_1 ]
     ret = [ peter_graph( ) ]
     for _ in range(_sage_const_4 ):
         code = peter_premu(code)
         ret += [  peter_graph(code)]
     return ret
 
 def cycle_graph():
     nodes = _sage_const_14 
     cycle = graphs.CycleGraph(nodes)
     code = [_sage_const_1 ] * nodes
     return tanner_graph(cycle, code)
 
 
except:
 _st_.goboom(_sage_const_83 )
_st_.blockend()
_st_.current_tex_line = _sage_const_63 
_st_.blockbegin()
try:
 
 
 ggs = peter_graphs()
 ff = cycle_graph()
 for gg in ggs:
   gg.set_latex_options(
           edge_label_sloped = False,
           edge_labels=True,
           edge_thickness=_sage_const_0p005 ,
           vertex_labels=False,
           vertex_size= _sage_const_0p01 ,
           format='dot2tex',
           prog='crico',
           graphic_size=(_sage_const_7 ,_sage_const_7 ),
           edge_fills=False,
       )
 ff.set_latex_options(
           edge_label_sloped = False,
           edge_labels=True,
           edge_thickness=_sage_const_0p005 ,
           vertex_labels=False,
           vertex_size= _sage_const_0p01 ,
           format='dot2tex',
           prog='crico',
           graphic_size=(_sage_const_30 ,_sage_const_8 ),
           edge_fills=False,
       )
 
 ops = [ gg.latex_options() for gg in ggs ]
 ops2 = ff.latex_options()
 
 graphs_tex =  ' \ \ \ '.join([  str(op.tkz_picture())  for op in ops[:_sage_const_3  ]])
 graphs_tex_2 = ' \ \ \ \ \ ' +  ' \ \ \ '.join([  str(op.tkz_picture())  for op in ops[_sage_const_3 :]])
 graphs_tex_ff  = str(ops2.tkz_picture())
except:
 _st_.goboom(_sage_const_98 )
_st_.blockend()
try:
 _st_.current_tex_line = _sage_const_104 
 _st_.inline(_sage_const_0 , graphs_tex)
except:
 _st_.goboom(_sage_const_104 )
try:
 _st_.current_tex_line = _sage_const_107 
 _st_.inline(_sage_const_1 , graphs_tex_2)
except:
 _st_.goboom(_sage_const_107 )
try:
 _st_.current_tex_line = _sage_const_140 
 _st_.inline(_sage_const_2 , graphs_tex_ff)
except:
 _st_.goboom(_sage_const_140 )

