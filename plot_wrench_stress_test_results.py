#!/usr/bin/env python3
import sys
import math
import ast
import statistics
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

data={'2.0': [[0.66], [21.84765625]], '2.1': [[0.64], [21.7265625]], '1.0': [[3.56], [130.51171875]], '1.7': [[0.74], [132.6484375]], '1.9': [[0.49], [131.29296875]], 'experimental': [[1.74], [140.73828125]], '1.8': [[0.6], [131.75390625]], '1.6': [[0.68], [132.64453125]], '1.1': [[4.37], [125.10546875]], 'master': [[1.6], [37.94140625]], '2.2': [[1.57], [38.00390625]], '1.11': [[0.55], [132.015625]], '1.10': [[0.55], [131.77734375]], '1.4': [[0.46], [19.734375]], '1.3': [[0.4], [18.62890625]], '1.2': [[0.49], [123.4921875]]}





fontsize = 18

output_file = "results.pdf"

sys.stderr.write("Generating " + output_file + "...\n")

f, ax1 = plt.subplots(1, 1, sharey=True, figsize=(14,7))

plt.grid(axis='y')

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
ax1.set_yscale("log")
yticks = [10,20, 50, 100, 200, 400, 800]
ax1.set_yticks(yticks)
ax1.set_yticklabels([str(t) for t in yticks])
ax1.set_ylim([10, 830])
ax2.set_ylim([0, 800])

#print(ax1.get_yticks())

ax1.set_xlabel("WRENCH versions",fontsize=fontsize+1)
ax1.set_ylabel("Simulation time (sec)",fontsize=fontsize+1)
ax2.set_ylabel("Maximum RSS (MB)",fontsize=fontsize+1)

ax1.tick_params(axis='x', labelsize=fontsize)
ax1.tick_params(axis='y', labelsize=fontsize)
ax2.tick_params(axis='y', labelsize=fontsize)

lns = lns1+lns2
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=0, fontsize=fontsize)

plt.tight_layout()
plt.savefig(output_file)
plt.close()

sys.stderr.write("Plot saved to file " + output_file + "\n")

