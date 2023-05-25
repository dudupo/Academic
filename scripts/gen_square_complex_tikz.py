from random import random 
from itertools import product 
def tikz(n,m):
    
    ret = """ \\begin{figure}[H]
            %\\label{fig:square}
            \\begin{center}
            \\begin{tikzpicture}
            \\draw[thick]"""
    ret += "(0,0)"
    nodes = "\\node[below left] at (0,0) {$ (g,+)$}; "
    
    anodes = [ ] #  for _ in range(m):
    anodesp = [ ] 
    for _ in range(m):
        ya, xa = random() * 1.2 ,4 + random()*2
        anodes += [ f"({xa},{ya}) -- (0,0)" ]
        anodesp += [ (xa,ya) ] 
    bnodes, cnodes  = [ ], [ ] 
    bnodesp, cnodesp  = [ ], [ ] 
    def update_node(x0, y0, sign, _list):
        y, x1 = sign + random() * 5 * sign ,random()*5
        x2 = x1 + 2.5#random()*2
        _list += [ (x0+ x1,y0+ y)] 
        return [f"(0,0)  -- ({x1}, {y}) -- ({x2}, {y})"]  
    for __ in range(n):
       bnodes += update_node(0,0,1, bnodesp)
       cnodes += update_node(0,0,-1, cnodesp)

            #(0,0) -- (0,2) -- (2,2) -- (2,0) -- (0,0) -- (1, 3) -- (3 ,3) -- (2,0) --  (0,0);"      
        #'''     
        #    nodes += f"\n \\node[above left] at ({x1},{y}) {$ (gb_{__},-)$};
        #            \n\\node[above right] at ({x2},{y}) {$ (a_{_}gb_{__},+)$};
        #    \\node[below right] at (2,0) {$ (ag,-)$};
        #    \\node[above left] at (1,3) {$ (gc,-)$};
        #    \\node[above right] at (3,3) {$ (agc,+)$};
        #
        #'''
    def gen_agb_nodes(_anodesp, _bnodesp, sign, sym, coff, hist=(0,0), g="g"):
        ret, latex, nodes = [], "", ""
        for ((i,(xa, ya)), (j,(xb, yb))) in product(enumerate(_anodesp), enumerate(_bnodesp)):
            p = (xa+coff*(j+1), yb+ coff *sign *(j+1))
            ret += [p] 
            latex += f"{hist} -- ({xb},{yb}) -- ({p[0]},{p[1]}) -- ({xa},{ya}) -- {hist}\n"
            vertex = f"{{$ a_{{ {i}  }} {g}{sym}_{{ {j} }} $}}"
            nodes += f"\\node at ({p[0]+0.1},{p[1]+0.2*i}) {vertex};\n"
        return ret, latex, nodes
    from random import randint 
    abnodesp, lat1, latnode1  = gen_agb_nodes(anodesp, bnodesp, 1, "b", 0.6)
    acnodesp, lat2, latnode2  = gen_agb_nodes(anodesp, cnodesp, -1, "c", 0.6)
    second_order = 1 #randint(0,m-1)    
    aanodesp = [ ]
    for _ in range(m):
        ya, xa = random() * 1.2 ,4 + random()*2
        aanodesp += [ ( anodesp[second_order][0] +  xa, anodesp[second_order][1] + ya) ] 

    sabnodesp, lat3, lat3node3 = gen_agb_nodes(aanodesp, abnodesp[n* second_order: n* second_order + n], 1, "b" , 0.9, hist = anodesp[second_order], g = f"a_{{ {second_order} }}g")
    

    sacnodesp, lat4, lat3node4 = gen_agb_nodes(aanodesp, acnodesp[n* second_order: n* second_order + n], 1, "c" , 0.9,  anodesp[second_order], g = f"a_{{ {second_order} }}g")
    ret += lat1 + lat2 + lat3 +  lat4 + ";\n" + latnode1 + latnode2 + lat3node3 + lat3node4  
    ret += "\\node at (-0.1,0) {$ g $};\n"  
    for g, _alist in zip( ["g"], [anodesp]):# f"a_{{ {second_order} }}g"], [anodesp, aanodesp]): 
        for i, (x,y) in enumerate(_alist):
            ret += f"\\node at ({x+0.1},{y+0.1}) {{$ a_{{ {i} }}{g} $}};\n"
        for sym, _list in zip(["b" ,"c"] , [bnodesp, cnodesp]):
            for i, (x,y) in enumerate(_list):
                vertex = f"{{$ {g}{sym}_{{ {i} }} $}}" #if i % 2 == 0 else f"{{$ a_{{\\cdot}} g{sym}_{{ {i} }} $}}"
                ret +=  f"\\node at ({x+0.1},{y+0.1}) {vertex};\n"

    return ret + """
            \\end{tikzpicture}
            \\end{center}
            \\caption{Square of the complex, with edges $(g,ag), (agb, gb) \in E_A,
            (g,gb), (agb, ag) \in E_B.$ \label{fig:square}
            }
            \\end{figure}"""

def doc(include = False):

    pre = """ \\documentclass{article}
\\usepackage[utf8]{inputenc}
\\usepackage[a4paper, total={7in, 10in}]{geometry}
\\usepackage{braket}
\\usepackage{xcolor}
\\usepackage{amsmath}
\\usepackage{amssymb}
\\usepackage{amsfonts}
\\usepackage{graphicx}
\\usepackage{svg}
\\usepackage{float}
\\usepackage{tikz}
\\usepackage[ruled,vlined]{algorithm2e}
\\usepackage{multicol}
\\usepackage[backend=biber,style=alphabetic,sorting=ynt]{biblatex}
\\usepackage{xcolor}
%\\addbibresource{sample.bib} %Import the bibliography file

\\newcommand{\\commentt}[1]{\\textcolor{blue}{ \\textbf{[COMMENT]} #1}}
\\newcommand{\\ctt}[1]{\\commentt{#1}}
\\newcommand{\\prb}[1]{ \\mathbf{Pr} \\left[ {#1} \\right]}
\\newcommand{\\onotation}[1]{\\(\\mathcal{O} \\left( {#1}  \\right) \\)}
\\newcommand{\\ona}[1]{\\onotation{#1}}
\\newcommand{\\PSI}{{\\ket{\\psi}}}
\\newcommand{\\LESn}{\\ket{\\psi_n}}
\\newcommand{\\LESa}{\\ket{\\phi_n}}
\\newcommand{\\LESs}{\\frac{1}{\\sqrt{n}}\\sum_{i}{\\ket{\\left(0^{i}10^{n-i}\\right)^{n}}}}
\\newcommand{\\Hn}{\\mathcal{H}_{n}}
\\newcommand{\\Ep}{\\frac{1}{\\sqrt{2^n}}\\sum^{2^n}_{x}{ \\ket{xx}}}
\\newcommand{\\HON}{\\ket{\\psi_{\\text{honest}}}}
\\newcommand{\\Lemma}{\\paragraph{Lemma.}}


\\setlength{\\columnsep}{0.6cm}

\\newcommand{\\Gz}{ G_{z}^{\\delta} } 

\\begin{document}

\\title{Quantum LTC With Positive Rate}
\\author{David Ponarovsky}
\\maketitle
%\\begin{multicols*}{2}
\\newcommand{ \\Hw }{ \\delta\\Delta -\\Delta^{\\frac{1}{2}-\\varepsilon}/\\delta  }
	\\newcommand{ \\Nw }{ \\Delta^{\\frac{3}{2}-\\varepsilon}} 
	  \\newcommand{ \\Gu } { \\Gamma^{\\cup} }
	  \\newcommand{ \\Guq } { \\Gamma^{\\cup, \\square} }

    	\\newcommand{ \\Gsa } {\\Gamma_{\\square_{1}} }
	\\newcommand{ \\Gsb } {\\Gamma_{\\square_{2}} }
        \\newcommand{ \\Aa } { C_{A_{1}}}  
	\\newcommand{ \\Ab } { C_{A_{2}}}
	\\newcommand{ \\Ac } { C_{A_{3}}}
	\\newcommand{ \\Aab } { \\Aa \\otimes \\Ab } 
	\\newcommand{ \\Aac } { \\Aa \\otimes \\Ac }
	\\newcommand{ \\Aabc } { \\Aa \\otimes \\Ab \\otimes \\Ac }
	\\newcommand{ \\Aabp } { \\Aa^{\\perp} \\otimes \\Ab^{\\perp} } 
	\\newcommand{ \\Aacp } { \\Aa^{\\perp} \\otimes \\Ac^{\\perp} }
	\\newcommand{ \\Aabcp } { \\Aa^{\\perp} \\otimes \\Ab^{\\perp} \\otimes \\Ac^{\\perp} }
	\\newcommand{ \\Aabpp } { \\left( \\Aabp \\right)^\\perp } 
	\\newcommand{ \\Aacpp } { \\left( \\Aacp \\right)^\\perp }
	\\newcommand{ \\Aabcpp } { \\left( \\Aabcp \\right)^\\perp }
	\\newcommand{ \\YY } {  y_{1}y_{2}^{\\top} }
	\\newcommand{ \\ZZ } {  z_{1}z_{2}^{\\top} } 
	\\newcommand{ \\TT } { \\tilde{\\tau} } 


  \\paragraph{preamble.} preamble.  
 """ if not include else ""
    
    values = [ (2,3), (2,3) , (2,3) , (2,3) ] #, #(3,3) , (4,2), (5,3), (4,4) ]  
    
    for m,n in values:
        pre += tikz(n,m) +"\n"
    if include: 
        return pre
    return  pre + """ 
%\\end{multicols*}
  % \\printbibliography 
\\end{document}

 """


if __name__ == "__main__":
    #print(tikz(3,2))
    include = False#  True
    _file_name ="complex-include.tex" if include else "complex.tex" 
    open(f'../projects/NLTES_project/{_file_name}', 'w+').write( doc(include) )



