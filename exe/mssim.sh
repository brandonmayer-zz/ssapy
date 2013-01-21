#!/bin/bash

BASEDIR=$(dirname $0)

if [ `uname -o` = "Cygwin" ]
then
    python `cygpath -m $BASEDIR`/mssim.py "$@"
else
    python $BASEDIR/mssim.py "$@"
fi