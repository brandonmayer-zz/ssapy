#!/bin/bash

BASEDIR=$(dirname `which domJointLocal.sh`)

if [ `uname -o` = "Cygwin" ]
then
    python `cygpath -m $BASEDIR`/domJointLocal.py "$@"
else
    python ${BASEDIR}/domJointLocal.py "$@"
fi