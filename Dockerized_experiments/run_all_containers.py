#!/usr/bin/env python3 

import sys
import glob
import subprocess
from datetime import datetime

num_cs = 10
num_ss = 10
num_ps = 0
num_jobs = 20000
num_trials = 1

dockerfiles=sorted(glob.glob("Dockerfile_wrench_stress_test_*"))

data = {}

for f in dockerfiles:

    now = datetime.now()

    container = f[11:]
    sys.stderr.write("Running container " + container + "\n")
    maj_version = int(container[19:].split(".")[0])
    min_version = int(container[19:].split(".")[1])
    version_string = "v"+container[19:]
    times=[]
    mems=[]
    command = "docker run -it --rm " + container + " /usr/bin/time -v wrench-stress-test " + str(num_jobs) + " " + str(num_cs) + " " + str(num_ss) + " " + str(num_ps)
    if (maj_version == 1) and (min_version < 6) and (min_version > 1):
        command += " --wrench-no-log"
    if (maj_version == 2) and (min_version == 2):
#        command += " 0"
        command += " 10485760"
    for trial in range(0,num_trials):
        output = subprocess.check_output(command, shell=True).decode('utf-8').splitlines()
        for line in output:
            if "Elapsed (wall clock)" in line:
                tokens = line.split(":")
                times.append(float(60.0 * float(tokens[-2]) + float(tokens[-1])))
            elif "Maximum resident set size" in line:
                tokens = line.split(":")
                mems.append(float(tokens[-1]) / 1024.0)
    data[version_string] = [times, mems]
    now2 = datetime.now()
    #print(now2 - now)

# Sort
data = dict(sorted(data.items(), key=lambda item: int(item[0][1:].split(".")[0]) * 1000 + int(item[0][1:].split(".")[1])))
print(data)
