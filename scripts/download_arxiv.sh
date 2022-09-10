#!/bin/bash

source_dir="/home/davidponar/workspace/sources_of_others"
#~/workspace/sources_of_others/

# The identifier number number given by arxiv site.  
doc_numb="$1"
# The name to be stored. 
doc_name=$(echo "$source_dir/$2" | sed -e "s/ /-/g")
#echo "" > $doc_name
wget --output-document="$doc_name.gz" --user-agent="Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36" "https://arxiv.org/e-print/$doc_numb"

#for testing - 2202.13641 (Quantum Tanner Codes).

#mv "$source_dir/2202.13641" $doc_name 
gzip -d "$doc_name.gz"
file_type=$(file $doc_name) 
if [[  "$file_type"  == *"LaTeX"* ]]; then 
  mv $doc_name "$doc_name.tex"
elif [[ "$file_type" == *"tar"* ]]; then 
  mv $doc_name "$doc_name.tar" 
  tar -xvf "$doc_name.tar"
fi 


