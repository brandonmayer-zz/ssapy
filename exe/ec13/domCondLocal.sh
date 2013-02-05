#!/bin/bash

BASEDIR=$(dirname `which domCondLocal.sh`)

if [ `uname -o` = "Cygwin" ]
then
    python `cygpath -m $BASEDIR`/domCondLocal.py "$@"
else
    python ${BASEDIR}/domCondLocal.py "$@"
fi