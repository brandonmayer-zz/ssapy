#!/bin/bash

BASEDIR=$(dirname `which domMargLocalMc.sh`)

if [ `uname -o` = "Cygwin" ]
then
    python `cygpath -m $BASEDIR`/domMargLocalMc.py "$@"
else
    python ${BASEDIR}/domMargLocalMc.py "$@"
fi
