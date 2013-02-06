#!/bin/bash

BASEDIR=$(dirname `which domBidEval.sh`)

if [ `uname -o` = "Cygwin" ]
then
    python `cygpath -m ${BASEDIR}`/domBidEval.py "$@"
else
    python ${BASEDIR}/domBidEval.py "$@"
fi
