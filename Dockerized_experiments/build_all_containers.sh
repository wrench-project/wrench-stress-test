#!/bin/bash

set -e

DOCKERFILES=`ls Dockerfile_wrench_stress_test_*`

for FILE in $DOCKERFILES; do
    CONTAINERNAME=`echo $FILE | sed "s/Dockerfile_//"`
    echo Building container $CONTAINERNAME
    docker build -t $CONTAINERNAME . -f $FILE
done
