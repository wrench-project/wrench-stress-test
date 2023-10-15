#!/usr/bin/env python3 

import sys
import glob
import subprocess
from datetime import datetime

num_cs = 10
num_ss = 10
num_ps = 0
num_jobs = 10000
num_trials = 2

def key_sorting(item):
    if item[0] == "master":
        return 100000
    elif item[0] == "experimental":
        return 1000000
    elif item[0] == "deque":
        return 10000000
    else:
        major = item[0].split(".")[0]
        minor = item[0].split(".")[1]
        return int(major) * 100 + int(minor)

def run_experiments(images):
    data = {}
    
    for image in images:
    
        version_string = image.split("_")[-1]
        times=[]
        mems=[]

        # Get the wrench firs arg
        command = "docker run -it --rm " + image + " bash -c 'echo $WRENCH_FIRST_ARG'"
        wrench_first_arg = subprocess.check_output(command, shell=True).decode('utf-8').splitlines()[0]

        # Get the wrench logging env variable
        command = "docker run -it --rm " + image + " bash -c 'echo $WRENCH_LOGGING'"
        wrench_logging = subprocess.check_output(command, shell=True).decode('utf-8').splitlines()[0]

        # Get the wrench buffersize env variable
        command = "docker run -it --rm " + image + " bash -c 'echo $WRENCH_BUFFERSIZE'"
        wrench_buffersize = subprocess.check_output(command, shell=True).decode('utf-8').splitlines()[0]
        
        command = "docker run -it --rm " + image + " /usr/bin/time -v wrench-stress-test " + wrench_first_arg + " " + str(num_jobs) + " " + str(num_cs) + " " + str(num_ss) + " " + str(num_ps) + " " + wrench_logging + " " + wrench_buffersize
        sys.stderr.write("Running " + command + " (" + str(num_trials) + " times) ...\n")

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
    
    data = dict(sorted(data.items(), key= key_sorting))

    # Sort
    print(data)


if __name__ == "__main__":
    run_experiments(sys.argv[1:len(sys.argv)])
    


