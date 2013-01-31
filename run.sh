#!/bin/bash

# Name your first "bootstrap" environment:
INITIAL_ENV=py-env0
PWD=`pwd`
# Activate env.
source $INITIAL_ENV/bin/activate
# Export nltk data variable for use of lib.
export NLTK_DATA=${PWD}/nltk_data
# Change to correct directory and run app.
cd mirrorproject
# python main.py
python test.py
