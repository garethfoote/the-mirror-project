#!/bin/bash

source setup.cfg

LOG=${TARGET_DIR}env.log
# Log function.
function log {
    echo $1
    echo $1 >> $LOG
}

function getUrl {

    if [[ -n $(which wget) ]];
    then
        wget $1
    elif [[ -n $(which curl) ]];
    then
        curl -O $1
    else
        echo "[ERROR]No curl or wget! OMG!"
        echo "[ERROR]No curl or wget! OMG!" >> $LOG
        exit
    fi
}

# Get parameters
params="$(getopt -o d:h \
        -l exclude:,help,verbose \
            --name "$0" -- "$@")"
eval set -- "$params"
unset params

while true
do
    case $1 in
        -d|--directory)
            TARGET_DIR=`cd $2; pwd`/
            # Overwrite target directory in config.
            # sed '/TARGET_DIR=/d' ./setup.cfg > ./setup.tmp
            sed -i "2iTARGET_DIR=${TARGET_DIR}" setup.cfg
            # Re-source so varibles are reset.
            source setup.cfg
            shift 2
            ;;
        -h|--help)
            echo "There's no help for you here."
            exit
            ;;
        --)
            shift
            break
            ;;
    esac
done

# Select current version of virtualenv:
VERSION=1.10.1
# Options for your first environment:
ENV_OPTS='--no-site-packages --distribute'
# Set to whatever python interpreter you want for your first environment: (only tested with 2.7)
PYTHON=$(which python)
URL_BASE=http://pypi.python.org/packages/source/v/virtualenv
#log
touch $LOG

# --- Download virtual env ---
if [ ! -f virtualenv-$VERSION.tar.gz ];
then
    echo "Downloading: $URL_BASE/virtualenv-$VERSION.tar.gz"
    getUrl $URL_BASE/virtualenv-$VERSION.tar.gz
fi
if [ ! -f virtualenv-$VERSION.tar.gz ];
then
    log "[ERROR]File does not exist. Either did not download or curl/wget not installed."
    exit
fi

# --- Extract, install and activate env ---
tar xzf virtualenv-$VERSION.tar.gz
# Create the first "bootstrap" environment.
log "[INFO]Initial virtual env install: $INITIAL_ENV"
$PYTHON virtualenv-$VERSION/virtualenv.py $INITIAL_ENV
# Don't need this anymore.
rm -rf virtualenv-$VERSION
# Install virtualenv into the environment.
$INITIAL_ENV/bin/pip install virtualenv-$VERSION.tar.gz
# Activate env.
source $INITIAL_ENV/bin/activate

# --- Check install was successful and tidy ---
PYTHONEXEC=`python -c "import sys; print sys.executable"`
PYTHONENVDIR=${PYTHONEXEC/\/${INITIAL_ENV}\/bin\/python/""}
PWD=`pwd`
# Is python executable in this directory opposed to e.g. /usr/bin
if [ "$PWD" == "$PYTHONENVDIR" ]; then
    log "[*]virtualenv installation successful! \o/"
    # Tidying.
    rm virtualenv-$VERSION.tar.gz
fi

# Install python-dev if on Linux. Hoping it is present on OSx.
if [[ "$(uname -s)" == *Linux* ]]
then
    log "[INFO]Installing python dev.";
    sudo apt-get install python-dev libxml2-dev libxslt-dev
elif [[ "$(uname -s)" == *Darwin* ]] 
then

    # Notify the gcc (C compiler) is missing
    if [[ ! -n $(which gcc) ]];
    then
        log "[ERROR] Missing GNU C Compiler (GCC). Download and install appropriate pkg for your operating system here: https://github.com/kennethreitz/osx-gcc-installer/downloads"
        exit
    fi
    log "[INFO]Darwin (OSx) - Do not install python-dev"
fi

# --- Install python dependencies ---
if [ ! -f requirements.txt ]
then
    log "[ERROR]requirements.txt does not exist."
    exit
fi
log "[INFO]Installing PIP requirements"
pip install -r requirements.txt
if [ ! -d "${TARGET_DIR}nltk_data" ]; then

    log "[INFO]Downloading NLTK data to ${TARGET_DIR}nltk_data"
    # Install nltk data. (This will take a while)
    python -m nltk.downloader -d ${TARGET_DIR}nltk_data all
fi
