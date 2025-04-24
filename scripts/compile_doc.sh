#!/bin/sh
pdflatex  --shell-escape $1
filename=`basename $1 .tex`
biber $filename
pdflatex  --shell-escape $1
mv $filename.pdf  ~/workspace/Academic/projects/pdfs/

if [ ! -d "./logs" ]; then
 mkdir "./logs"
fi

for ext in aux bcf log run.xml bbl blg tex.bbl tex.blg; do 
 mv *.$ext ./logs/
done

Date=`date`
git add $filename.tex  ~/workspace/Academic/projects/pdfs/$filename.pdf
git add *.tex 
git commit -m "compiling $filenaem-$Date"

if [ ! -d "./my-bib-file/" ]; then
  if [ ! -d "~/workspace/my-bib-file/" ]; then
    git clone git@github.com:dudupo/my-bib-file.git ~/workspace/my-bib-file
  fi
  ln -s ~/workspace/my-bib-file 
  ln ~/workspace/my-bib-file/sample.bib
fi 

( cd ./my-bib-file/ ; git add ./sample.bib ; git commit -m "compiling bib - $Date" ) 


