#!/usr/bin/env python3
import sys
import math
import ast
import statistics
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

data={'1.0': [[24.8, 23.32], [312.51171875, 312.57421875]], '1.1': [[33.78, 34.7], [298.44140625, 298.59375]], '1.2': [[1.26, 1.28], [294.34765625, 294.34375]], '1.3': [[1.05, 1.08], [31.453125, 31.4375]], '1.4': [[1.2, 1.22], [33.83984375, 33.7890625]], '1.5': [[1.69, 1.7], [312.82421875, 312.80859375]], '1.6': [[1.75, 1.76], [314.87109375, 314.95703125]], '1.7': [[1.89, 1.86], [315.1640625, 315.34375]], '1.8': [[1.92, 1.92], [314.19140625, 314.28125]], '1.9': [[1.64, 1.63], [313.7734375, 313.8125]], '1.10': [[1.76, 1.75], [314.88671875, 314.8359375]], '1.11': [[1.75, 1.75], [314.796875, 314.859375]], '2.0': [[1.71, 1.7], [35.8125, 35.8515625]], '2.1': [[1.75, 1.68], [36.0546875, 35.84375]], '2.2': [[4.05, 4.07], [75.6328125, 75.65234375]], 'master': [[4.03, 4.06], [75.62890625, 75.62109375]], 'experimental': [[4.56, 4.6], [323.328125, 323.328125]]}







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

