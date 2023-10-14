#!/usr/bin/env python3
import sys
import math
import ast
import statistics
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

data={'1.0': [[0.09, 0.09], [15.51171875, 15.44140625]], '1.1': [[0.08, 0.07], [15.2265625, 15.37109375]], '1.2': [[0.03, 0.03], [15.83203125, 15.58203125]], '1.3': [[0.02, 0.02], [10.50390625, 10.6953125]], '1.4': [[0.03, 0.03], [10.67578125, 10.5546875]], '1.5': [[0.04, 0.04], [16.7265625, 16.55859375]], '1.6': [[0.04, 0.04], [17.28515625, 17.19140625]], '1.7': [[0.04, 0.04], [17.171875, 17.234375]], '1.8': [[0.03, 0.03], [16.3046875, 16.20703125]], '1.9': [[0.03, 0.03], [15.734375, 15.6953125]], '1.10': [[0.03, 0.03], [16.3515625, 16.31640625]], '1.11': [[0.03, 0.03], [16.2890625, 16.30859375]], '2.0': [[0.04, 0.04], [12.63671875, 12.5234375]], '2.1': [[0.04, 0.04], [12.7578125, 12.71875]], '2.2': [[0.09, 0.09], [14.6796875, 14.66796875]], 'master': [[0.09, 0.08], [14.60546875, 14.60546875]], 'experimental': [[0.1, 0.09], [25.6484375, 25.6484375]]}






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
#ax1.set_ylim([10, 830])
#ax2.set_ylim([0, 800])

#print(ax1.get_yticks())

ax1.set_xlabel("WRENCH versions",fontsize=fontsize+1)
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

