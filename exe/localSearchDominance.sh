#!/bin/bash

BASEDIR=$(dirname $0)

if [ `uname -o` = "Cygwin" ]
then
    python `cygpath -m $BASEDIR`/localSearchDominance.py "$@"
else
    python $BASEDIR/localSearchDominance.py "$@"
fi