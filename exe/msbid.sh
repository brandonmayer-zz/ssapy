#!/bin/bash

BASEDIR=$(dirname $0)

if [ `uname -o` = "Cygwin" ]
then
    python `cygpath -m $BASEDIR`/msbid.py "$@"
else
    python $BASEDIR/msbid.py "$@"
fi