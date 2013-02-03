#!/bin/bash

BASEDIR=$(dirname `which jtc.sh`)

if [ `uname -o` = "Cygwin" ]
then
    python `cygpath -m $BASEDIR`/jgcorr.py "$@"
else
    python ${BASEDIR}/jgcorr.py "$@"
fi