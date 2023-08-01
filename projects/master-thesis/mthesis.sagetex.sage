## -*- encoding: utf-8 -*-
## This file (mthesis.sagetex.sage) was *autogenerated* from mthesis.tex with sagetex.sty version 2021/10/16 v3.6.
import sagetex
_st_ = sagetex.SageTeXProcessor('mthesis', version='2021/10/16 v3.6', version_check=True)
_st_.current_tex_line = 1
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
   ret = [ [ (X[0][0], X[0][1])  ] ]
   for x,y in X[1:]:
     if abs(y - ret[-1][-1][1]) > 1:
         ret[-1].append((x,17))
         ret +=  [ [ (x,y) ] ]
     else:
         ret[-1].append( (x,y) )
   return ret
 
 def colorgen():
   colors_list = ['gray', 'black']
   i = -1
   while True:
       i=  mod(i + 1, len(colors_list))
       yield colors_list[ i ]
 _colorgen = colorgen()
 
 def finate_poly_plot(fun, end=17):
   _color = next(_colorgen)
   point_lists =  split_lines([ (y, fmod(fun(y),end)) for y in linspace(0,end+2,3000) ])
   pplot_lines =  line(point_lists[0], color=_color, aspect_ratio=0.3)
   for _point_list in point_lists[1:]:
     pplot_lines += line(_point_list, color=_color, aspect_ratio=0.3)
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
     graph.set_edge_label(*edge[:2], f'{code[i]}')
   return graph
 
 def peter_premu(x):
     premu = [1,9,7,0,2,3,4,5,6,8,13,14,10,11,12]
     premuinv = [ 0 for _ in range(15) ]
     for i in range(15):
         for j in range(15):
             if premu[j] == i:
                 premuinv[i] = j
     return [ x[premuinv[i]] for i in range(15) ]
 
 def peter_graph(code = [0,1,1,0,0,1,1,0,1,1,0,1,0,0,1]):
   #code = list(range(15)) #[0,1,1,0,0,1,1,0,1,1,0,1,0,0,1]
   peter = graphs.PetersenGraph()
   return tanner_graph(peter, code)
 
 def peter_graphs():
     code = [0,1,1,0,0,1,1,0,1,1,0,1,0,0,1]
     ret = [ peter_graph( ) ]
     for _ in range(4):
         code = peter_premu(code)
         ret += [  peter_graph(code)]
     return ret
 
 def cycle_graph():
     nodes = 14
     cycle = graphs.CycleGraph(nodes)
     code = [1] * nodes
     return tanner_graph(cycle, code)
 
 
except:
 _st_.goboom(83)
_st_.blockend()
_st_.current_tex_line = 63
_st_.blockbegin()
try:
 
 
 ggs = peter_graphs()
 ff = cycle_graph()
 for gg in ggs:
   gg.set_latex_options(
           edge_label_sloped = False,
           edge_labels=True,
           edge_thickness=0.005,
           vertex_labels=False,
           vertex_size= 0.01,
           format='dot2tex',
           prog='crico',
           graphic_size=(7,7),
           edge_fills=False,
       )
 ff.set_latex_options(
           edge_label_sloped = False,
           edge_labels=True,
           edge_thickness=0.005,
           vertex_labels=False,
           vertex_size= 0.01,
           format='dot2tex',
           prog='crico',
           graphic_size=(30,8),
           edge_fills=False,
       )
 
 ops = [ gg.latex_options() for gg in ggs ]
 ops2 = ff.latex_options()
 
 graphs_tex =  ' \ \ \ '.join([  str(op.tkz_picture())  for op in ops[:3 ]])
 graphs_tex_2 = ' \ \ \ \ \ ' +  ' \ \ \ '.join([  str(op.tkz_picture())  for op in ops[3:]])
 graphs_tex_ff  = str(ops2.tkz_picture())
except:
 _st_.goboom(98)
_st_.blockend()
try:
 _st_.current_tex_line = 104
 _st_.inline(0, graphs_tex)
except:
 _st_.goboom(104)
try:
 _st_.current_tex_line = 107
 _st_.inline(1, graphs_tex_2)
except:
 _st_.goboom(107)
_st_.current_tex_line = 20
_st_.blockbegin()
try:
 R.<t> = PowerSeriesRing(GF(17));
 polyf = (t-1) * (t-2)
 polyg = (t-1) * (t-4)
 f(x) = (x-1) * (x-2)
 g(x) = (x-1) * (x-4)
 pplot_t = finate_poly_plot(f)
 pplot_t2 = finate_poly_plot(g)
except:
 _st_.goboom(28)
_st_.blockend()
try:
 _st_.current_tex_line = 31
 _st_.plot(0, format='notprovided', _p_= pplot_t + pplot_t2 )
except:
 _st_.goboom(31)
try:
 _st_.current_tex_line = 32
 _st_.inline(2, print_capt('$' + latex(f) + '$ and $' + latex(g) +'$'))
except:
 _st_.goboom(32)
_st_.current_tex_line = 187
_st_.blockbegin()
try:
 latex.matrix_delimiters('[', ']')
 M = matrix(GF(2), [1 for _ in range(3)])
 repetition = codes.LinearCode(M)
 H = repetition.parity_check_matrix().stack( matrix(GF(2), [1,1,0]))
 H1 = identity_matrix(3).tensor_product(H).augment( H.transpose().tensor_product(identity_matrix(3)))
 Hstr = latex(H)
 H1str = latex(H1)
except:
 _st_.goboom(195)
_st_.blockend()
try:
 _st_.current_tex_line = 204
 _st_.inline(3, Hstr)
except:
 _st_.goboom(204)
try:
 _st_.current_tex_line = 204
 _st_.inline(4, H1str)
except:
 _st_.goboom(204)
try:
 _st_.current_tex_line = 204
 _st_.inline(3, Hstr)
except:
 _st_.goboom(204)
try:
 _st_.current_tex_line = 204
 _st_.inline(4, H1str)
except:
 _st_.goboom(204)
_st_.endofdoc()
