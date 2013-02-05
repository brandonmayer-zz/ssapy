#!/bin/bash

BASEDIR=$(dirname `which domCondLocalZero.sh`)

if [ `uname -o` = "Cygwin" ]
then
    python `cygpath -m $BASEDIR`/domCondLocalZero.py "$@"
else
    python ${BASEDIR}/domCondLocalZero.py "$@"
fi