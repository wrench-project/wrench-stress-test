#!/usr/bin/env python3
import sys
import math
import ast
import statistics
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

data={'2.2/3.34': [[35.84, 36.54, 35.8, 35.82, 35.78], [649.96484375, 649.8515625, 649.91796875, 649.90234375, 649.8671875]], 'master/3.34': [[36.05, 35.98, 35.41, 35.81, 35.82], [616.234375, 616.30078125, 616.2421875, 616.33203125, 616.390625]], 'simgrid_master/master': [[33.73, 33.49, 33.34, 33.81, 33.76], [134.24609375, 134.25, 134.26953125, 134.47265625, 134.26171875]]}











fontsize = 18

output_file = "results.pdf"

sys.stderr.write("Generating " + output_file + "...\n")

f, ax1 = plt.subplots(1, 1, sharey=True, figsize=(14,7))

#plt.grid(axis='y')

x = list(range(0, len(data)))
    
y_time = []
y_mem = []
max_cv = 0
for key in data:
    cv_time = 100.0* statistics.stdev(data[key][0])/(sum(data[key][0])/len(data[key][0]))
    max_cv = max(max_cv, cv_time)
    cv_mem = 101.0* statistics.stdev(data[key][1])/(sum(data[key][1])/len(data[key][1]))
    max_cv = max(max_cv, cv_mem)
    y_time.append(sum(data[key][0])/len(data[key][0]))
    y_mem.append(sum(data[key][1])/len(data[key][1]))

print("Max %CV = " + str(max_cv))


lns1 = ax1.plot(x, y_time, 'bo-', markersize=12, linewidth=4, label="time")

ax2 = ax1.twinx()

lns2 = ax2.plot(x, y_mem, 'rs-', markersize=12, linewidth=4, label="memory")

x_index = 0
for key in data:
    min_time = math.inf
    max_time = 0
    for time in data[key][0]:
        min_time = min(min_time, time)
        max_time = max(max_time, time)
    ax1.plot([x_index, x_index],[min_time, max_time],'b-')
    min_mem = math.inf
    max_mem = 0
    for mem in data[key][1]:
        min_mem = min(min_mem, mem)
        max_mem = max(max_mem, mem)
    ax2.plot([x_index, x_index],[min_mem, max_mem],'r-')
    x_index += 1


plt.xticks(x, [str(y) for y in data.keys()])
#ax1.set_yscale("log")
#yticks = [10,20, 50, 100, 200, 400, 800]
#ax1.set_yticks(yticks)
#ax1.set_yticklabels([str(t) for t in yticks])
#ax1.set_ylim([20, 50])
#ax2.set_ylim([0, 400])

#print(ax1.get_yticks())

ax1.set_xlabel("WRENCH/SimGrid versions",fontsize=fontsize+1)
ax1.set_ylabel("Simulation time (sec)",fontsize=fontsize+1)
ax2.set_ylabel("Maximum RSS (MB)",fontsize=fontsize+1)

ax1.tick_params(axis='x', labelsize=fontsize)
ax1.set_xticklabels(data.keys(), rotation=45, fontsize=fontsize - 2)
ax1.tick_params(axis='y', labelsize=fontsize)
ax2.tick_params(axis='y', labelsize=fontsize)

lns = lns1+lns2
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=0, fontsize=fontsize)

plt.tight_layout()
plt.savefig(output_file)
plt.close()

sys.stderr.write("Plot saved to file " + output_file + "\n")

