\begin{sagesilent}
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
    if (abs(y - ret[-1][-1][1])) > 1 and (y < 5):
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
  point_lists =  split_lines([ (y, fmod(fun(y),end)) for y in linspace(0,end,3000) ])
  pplot_lines =  line(point_lists[0], color=_color) 
  for _point_list in point_lists[1:]:
    pplot_lines += line(_point_list, color=_color) 
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


\end{sagesilent}
