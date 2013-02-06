#!/bin/bash

# BASEDIR=$(dirname `which domBidEval.sh`)
SCRIPT=$(which domBidEval.sh)

if [ `uname -o` = "Cygwin" ]
then
    python $(cygpath -m ${SCRIPT}) "$@"
else
    python ${SCRIPT} "$@"
fi
