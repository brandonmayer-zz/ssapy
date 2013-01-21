#!/bin/bash

BASEDIR=$(dirname $0)

if [ `uname -o` = "Cygwin" ]
then
    python `cygpath -m $BASEDIR`/jgcorr.py "$@"
else
    python $BASEDIR/jgcorr.py "$@"
fi