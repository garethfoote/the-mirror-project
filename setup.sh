#!/bin/bash

# Select current version of virtualenv:
VERSION=1.8.4
# Name your first "bootstrap" environment:
INITIAL_ENV=py-env0
# Options for your first environment:
ENV_OPTS='--no-site-packages --distribute'
# Set to whatever python interpreter you want for your first environment:
PYTHON=$(which python)
URL_BASE=http://pypi.python.org/packages/source/v/virtualenv

# --- Real work starts here ---
tar xzf virtualenv-$VERSION.tar.gz
# Create the first "bootstrap" environment.
$PYTHON virtualenv-$VERSION/virtualenv.py $ENV_OPTS $INITIAL_ENV
# Don't need this anymore.
rm -rf virtualenv-$VERSION
# Install virtualenv into the environment.
$INITIAL_ENV/bin/pip install virtualenv-$VERSION.tar.gz
# Activate env.
source $INITIAL_ENV/bin/activate
# Check that hte python execuatble is running from here.
PYTHONEXEC=`python -c "import sys; print sys.executable"`
PYTHONENVDIR=${PYTHONEXEC/\/${INITIAL_ENV}\/bin\/python/""}
PWD=`pwd`
if [ "$PWD" == "$PYTHONENVDIR" ]; then
    echo "[*]virtualenv installation successful! \o/"
fi

# Install all python dependencies.
if [ ! -f requirements.txt ]
then
    echo "[x]requirements.txt does not exist."
    exit
fi
pip install -r requirements.txt

# Install nltk data.
python -m nltk.downloader -d $PWD/nltk_data all
