#!/bin/bash

BASEDIR=$(dirname `which domJointLocalMc.sh`)

if [ `uname -o` = "Cygwin" ]
then
    python `cygpath -m $BASEDIR`/domJointLocalMc.py "$@"
else
    python ${BASEDIR}/domJointLocalMc.py "$@"
fi
