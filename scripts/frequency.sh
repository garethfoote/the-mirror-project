#!/bin/bash
# Pass in directory and this will cat all text
# files and work out frequency of tag classes.
source ../env/bin/activate
export NLTK_DATA=$(pwd)/../nltk_data
cat ${1}*.txt > all.txt
python frequency.py
rm all.txt
