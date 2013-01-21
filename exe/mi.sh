#!/bin/bash

BASEDIR=$(dirname $0)

if [ `uname -o` = "Cygwin" ]
then
    python `cygpath -m $BASEDIR`/mi.py "$@"
else
    python $BASEDIR/mi.py "$@"
fi