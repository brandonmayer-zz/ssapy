#!/bin/bash

BASEDIR=$(dirname `which domCondMVLocal.sh`)

if [ `uname -o` = "Cygwin" ]
then
    python `cygpath -m $BASEDIR`/domCondLocalLimit.py "$@"
else
    python ${BASEDIR}/domCondLocalLimit.py "$@"
fi