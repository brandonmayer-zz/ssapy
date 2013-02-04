#!/bin/bash

BASEDIR=$(dirname `which domMargLocal.sh`)

if [ `uname -o` = "Cygwin" ]
then
    python `cygpath -m $BASEDIR`/domMargLocal.py "$@"
else
    python ${BASEDIR}/domMargLocal.py "$@"
fi