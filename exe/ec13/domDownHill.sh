#!/bin/bash

BASEDIR=$(dirname `which domDownHill.sh`)

if [ `uname -o` = "Cygwin" ]
then
    python `cygpath -m $BASEDIR`/domDownHill.py "$@"
else
    python ${BASEDIR}/domDownHill.py "$@"
fi
