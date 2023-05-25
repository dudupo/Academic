#!/bin/sh
pdflatex  --shell-escape $1
filename=`basename $1 .tex`
biber $filename
sage $filename.sagetex.sage
pdflatex  --shell-escape $1
mv $filename.pdf  ~/workspace/academic/projects/pdfs/

if [ ! -d "./logs" ]; then
 mkdir "./logs"
fi

for ext in aux bcf log run.xml bbl blg tex.bbl tex.blg; do 
 mv *.$ext ./logs/
done

if [ -e  git-update.list ] 
then
  value=`cat git-update.list`
  git add $value
fi  

Date=`date`
git add $filename.tex  ~/workspace/academic/projects/pdfs/$filename.pdf

for ext in tex py sage sh list vim; do 
  git add "*.$ext"
done 
git commit -m "compiling $filenaem-$Date"
