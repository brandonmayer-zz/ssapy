#!/bin/bash

BASEDIR=$(dirname `which domCondMVLocal.sh`)

if [ `uname -o` = "Cygwin" ]
then
    python `cygpath -m $BASEDIR`/domCondMVLocal.py "$@"
else
    python ${BASEDIR}/domCondMVLocal.py "$@"
fi