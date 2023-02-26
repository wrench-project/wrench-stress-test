#!/bin/bash

for dockerid in `cat ./wrench_versions.txt`; do
	cat ./TEMPLATE_Dockerfile_wrench_stress_test | sed "s/DOCKERID/$dockerid/" | > /tmp/Dockerfile_experiment
	echo $dockerid
	./build_all_containers.sh 1> /dev/null 2> /dev/null
	./run_all_containers.py 2> /dev/null
done


