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


if (len(sys.argv) != 3):
    sys.stderr.write("Usage: " + sys.argv[0] + " <wrench commit id> <wrench-stress-test commit id>\n")
    sys.exit(1)

dockerid = "wrench_stress_test"
dockerfile_template = "TEMPLATE_Dockerfile_wrench_stress_test"
dockerfile = "Dockerfile_wrench_stress_test"

# Create docker file
with open("./" + dockerfile_template) as file:
    lines = [line for line in file]
    output_lines = []
    for line in lines:
        if "WRENCH_COMMIT_ID" in line:
            output_lines.append(line.replace("WRENCH_COMMIT_ID", sys.argv[1]))
        elif "WRENCHSTRESSTEST_COMMIT_ID" in line:
            output_lines.append(line.replace("WRENCHSTRESSTEST_COMMIT_ID", sys.argv[2]))
        else:
            output_lines.append(line)

    with open("./" + dockerfile, "w") as outputfile:
        outputfile.writelines(output_lines);

# Build docker file
cmd = "docker build -t " + dockerid + " -f " + "./" + dockerfile + " ."
build_cmp = subprocess.run(cmd.split(" "), capture_output=False, stderr=subprocess.DEVNULL)
build_cmp.check_returncode()

# Run docker file
cmd = "docker run -it --rm " + dockerid + " /usr/bin/time -v wrench-stress-test " + str(num_jobs) + " " + str(num_cs) + " " + str(num_ss) + " " + str(num_ps)
run_cmd = subprocess.run(cmd.split(" "), capture_output=True, text=True)
if run_cmd.stdout == '':
    raise CalledProcessError(run_cmd.returncode, run_cmd.args)
run_cmd.check_returncode()

elapsed = 0
rss = 0
for line in run_cmd.stdout.splitlines():
    if "Elapsed (wall clock)" in line:
        tokens = line.split(":")
        elapsed =float(60.0 * float(tokens[-2]) + float(tokens[-1]))
    elif "Maximum resident set size" in line:
        tokens = line.split(":")
        rss = float(tokens[-1]) / 1024.0
print(sys.argv[1] + " " + str(elapsed) + " " + str(rss))
