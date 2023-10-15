#!/usr/bin/env python3
import sys
import math
import ast
import statistics
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

data={'1.0': [[65.59, 64.73, 64.5, 66.6, 66.05], [391.015625, 391.01953125, 391.015625, 391.05078125, 391.06640625]], '1.1': [[98.31, 100.57, 98.88, 98.47, 99.18], [368.609375, 368.60546875, 368.5859375, 368.65625, 368.6953125]], '1.2': [[2.87, 2.85, 2.84, 2.85, 2.84], [361.75390625, 361.65234375, 361.59375, 361.7265625, 361.609375]], '1.3': [[2.45, 2.46, 2.46, 2.45, 2.45], [44.875, 44.93359375, 44.91796875, 44.95703125, 44.9296875]], '1.4': [[2.69, 2.66, 2.74, 2.68, 2.66], [48.5625, 48.65625, 48.5625, 48.5390625, 48.62109375]], '1.5': [[3.31, 3.6, 3.33, 3.31, 3.37], [356.1171875, 356.34375, 356.1640625, 356.31640625, 356.2578125]], '1.6': [[3.58, 3.54, 3.52, 3.52, 3.53], [359.5, 359.28515625, 359.296875, 359.46484375, 359.32421875]], '1.7': [[3.68, 3.67, 3.72, 4.0, 3.69], [360.08203125, 360.0859375, 360.15625, 359.859375, 360.03125]], '1.8': [[3.39, 3.29, 3.39, 3.35, 3.35], [359.39453125, 359.18359375, 359.26171875, 359.390625, 359.30078125]], '1.9': [[2.99, 3.0, 2.99, 3.0, 2.91], [358.84375, 358.734375, 358.97265625, 358.79296875, 358.8359375]], '1.10': [[3.12, 3.11, 3.2, 3.09, 3.11], [360.0234375, 359.890625, 360.0234375, 359.9375, 359.890625]], '1.11': [[3.19, 3.17, 3.14, 3.18, 3.18], [359.89453125, 360.1640625, 359.84765625, 359.93359375, 360.0]], '2.0': [[2.55, 2.57, 2.55, 2.55, 2.55], [50.5234375, 50.4609375, 50.54296875, 50.2734375, 50.28515625]], '2.1': [[2.6, 2.56, 2.59, 2.56, 2.58], [50.828125, 50.7109375, 50.76171875, 50.59765625, 50.41015625]], '2.2': [[5.72, 5.66, 5.69, 5.72, 5.7], [110.7578125, 110.8359375, 110.8828125, 110.7421875, 110.70703125]], 'master': [[5.62, 5.67, 5.66, 5.62, 5.66], [110.63671875, 110.73046875, 110.765625, 110.71484375, 110.65625]], 'experimental': [[6.36, 6.31, 6.29, 6.35, 6.39], [501.9453125, 501.97265625, 502.1015625, 501.97265625, 501.91015625]]}








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
yticks = [10,20, 50, 100, 200, 400, 800]
ax1.set_yticks(yticks)
ax1.set_yticklabels([str(t) for t in yticks])
ax1.set_ylim([0, 50])
ax2.set_ylim([0, 400])

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

