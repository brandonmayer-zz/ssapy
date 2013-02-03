#!/bin/bash

BASEDIR=$(dirname `which jtc.sh`)

if [ `uname -o` = "Cygwin" ]
then
    python `cygpath -m $BASEDIR/jtc.py "$@"
else
    python ${BASEDIR}/jtc.py "$@"
fi