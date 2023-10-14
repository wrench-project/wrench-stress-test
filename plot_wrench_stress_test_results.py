#!/usr/bin/env python3
import sys
import math
import ast
import statistics
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

data={'2.0': [[1.29, 1.31], [30.91796875, 30.91796875]], '2.1': [[1.32, 1.31], [31.046875, 30.94921875]], '1.0': [[13.56, 17.19], [251.66796875, 251.703125]], '1.7': [[1.62, 1.63], [254.6640625, 254.68359375]], '1.9': [[1.35, 1.34], [253.015625, 253.08984375]], 'experimental': [[4.12, 4.08], [261.86328125, 261.859375]], '1.8': [[1.59, 1.6], [253.57421875, 253.5703125]], '1.6': [[1.54, 1.52], [254.13671875, 254.4140625]], '1.1': [[24.26, 19.17], [240.54296875, 240.578125]], 'master': [[3.14, 3.1], [62.48828125, 62.48828125]], '2.2': [[3.15, 3.17], [62.51171875, 62.51171875]], '1.11': [[1.3, 1.28], [253.9375, 253.8828125]], '1.10': [[1.29, 1.29], [253.9296875, 253.8984375]], '1.4': [[0.94, 0.93], [29.171875, 29.171875]], '1.3': [[0.83, 0.83], [26.9765625, 27.26953125]], '1.2': [[1.0, 1.01], [237.55859375, 237.41796875]], '1.5': [[1.35, 1.34], [252.53515625, 252.640625]]}





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
ax1.tick_params(axis='y', labelsize=fontsize)
ax2.tick_params(axis='y', labelsize=fontsize)

lns = lns1+lns2
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=0, fontsize=fontsize)

plt.tight_layout()
plt.savefig(output_file)
plt.close()

sys.stderr.write("Plot saved to file " + output_file + "\n")

