#!/bin/bash

source setup.cfg

LOG=the-mirror-env01.log
# Log function.
function log {
    echo $1
    echo $1 >> $LOG
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
            echo "There's no help for you here"
            exit
            ;;
        --)
            shift
            break
            ;;
    esac
done

# Select current version of virtualenv:
VERSION=1.8.4
LOG=the-mirror-env01.log
# Options for your first environment:
ENV_OPTS='--no-site-packages --distribute'
# Set to whatever python interpreter you want for your first environment:
PYTHON=python2.7
URL_BASE=http://pypi.python.org/packages/source/v/virtualenv
#log
touch $LOG

# --- Real work starts here ---
if [ ! -f virtualenv-$VERSION.tar.gz ];
then
    echo "Downloading!"
    if [[ -n $(which curl) ]];
    then
        curl -O $URL_BASE/virtualenv-$VERSION.tar.gz
    elif [[ -n $(which wget) ]];
    then
        wget $URL_BASE/virtualenv-$VERSION.tar.gz
    else
        echo "[ERROR]No curl or wget! OMG!"
        echo "[ERROR]No curl or wget! OMG!" >> $LOG
        exit
    fi
fi
if [ ! -f virtualenv-$VERSION.tar.gz ];
then
    log "[ERROR]File does not exist. Either did not download or curl/wget not installed."
    exit
fi
tar xzf virtualenv-$VERSION.tar.gz
# Create the first "bootstrkyp" environment.
log "[INFO]Initial virtual env install: $INITIAL_ENV"
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
    log "[*]virtualenv installation successful! \o/"
fi

# Install python-dev if on Linux. Hoping it is present on OSx.
if [[ "$(uname -s)" == *Linux* ]]
then
    log "[INFO]Installing python dev.";
    sudo apt-get install ${PYTHON}-dev libxml2-dev libxslt-dev
elif [[ "$(uname -s)" == *Darwin* ]] 
then
    STATIC_DEPS=true
    log "[INFO]Darwin (OSx) - Do not install python-dev"
fi

if [ ! -f requirements.txt ]
# Install python dependencies.
then
    log "[ERROR]requirements.txt does not exist."
    exit
fi
log "[INFO]Installing PIP requirements"
pip install -r requirements.txt

log "[INFO]Downloading NLTK data to ${TARGET_DIR}"
# Install nltk data.
python -m nltk.downloader -d ${TARGET_DIR}nltk_data all