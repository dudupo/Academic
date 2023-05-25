#!/bin/bash

(python ./control.py) | cat > ./control.qpic
qpic -f tex ./control.qpic 
qpic -f tikz ./control.qpic 
pdflatex ./control.tex 
zathura ./control.pdf
