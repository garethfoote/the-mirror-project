#!/bin/bash

source setup.cfg

echo "Config for the env: $INITIAL_ENV" >&2

# Activate env.
source $INITIAL_ENV/bin/activate
# Export nltk data variable for use of lib.
export NLTK_DATA=${PWD}/nltk_data 
# Change to correct directory and run app.
cd src
python main.py --type poemparse
