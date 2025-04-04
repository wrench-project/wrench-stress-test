#!/usr/bin/env python3
import sys
import math
import ast
import statistics
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

data={'1.7': [[47.62, 46.66, 46.72, 46.6, 48.07], [1177.1171875, 1176.94921875, 1176.76953125, 1176.796875, 1176.9296875]], '1.8': [[39.14, 38.55, 38.32, 38.8, 37.9], [1082.9765625, 1082.734375, 1082.94921875, 1082.74609375, 1082.7265625]], '1.9': [[18.03, 18.14, 17.9, 18.28, 18.32], [1082.40234375, 1082.3828125, 1082.37890625, 1082.49609375, 1082.4296875]], '1.10': [[19.74, 19.16, 19.72, 19.68, 19.45], [1085.01953125, 1084.98046875, 1084.84375, 1084.84375, 1085.015625]], '1.11': [[19.4, 19.21, 19.15, 19.54, 19.46], [1084.9921875, 1084.90234375, 1085.02734375, 1085.0625, 1084.9921875]], '2.0': [[13.88, 13.7, 13.82, 13.74, 13.7], [207.56640625, 207.31640625, 207.33203125, 207.078125, 207.30859375]], '2.1': [[13.78, 13.76, 13.64, 13.78, 13.71], [207.4140625, 207.703125, 207.59765625, 207.2890625, 207.47265625]], '2.2': [[14.68, 14.93, 14.63, 14.54, 14.56], [258.26953125, 258.26953125, 258.08984375, 258.1640625, 258.1796875]], 'master': [[14.64, 14.55, 14.51, 14.58, 14.44], [257.99609375, 258.06640625, 257.92578125, 258.1171875, 257.85546875]], 'experimental': [[13.29, 13.41, 13.28, 13.29, 13.4], [66.609375, 66.59375, 66.71484375, 66.5625, 66.59375]]}













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

