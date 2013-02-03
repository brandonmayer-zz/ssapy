#!/bin/bash

BASEDIR=$(dirname $0)

if [ `uname -o` = "Cygwin" ]
then
    python `cygpath -m $BASEDIR`/jtc.py "$@"
else
    SCRIPT=`which jtc.py`
    python $SCRIPT "$@"
fi