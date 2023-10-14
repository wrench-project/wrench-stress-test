#!/usr/bin/env python3
import sys
import math
import ast
import statistics
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

data={'v1.0': [[583.68, 583.04, 577.22, 575.11, 567.52, 573.45, 574.29, 574.18, 572.49, 573.82], [500.8125, 500.82421875, 500.72265625, 500.765625, 500.72265625, 500.6328125, 500.796875, 500.625, 500.7265625, 500.7578125]], 'v1.1': [[753.13, 752.15, 754.72, 748.61, 740.9, 747.83, 749.58, 743.92, 750.98, 749.46], [511.84765625, 511.74609375, 511.85546875, 511.96875, 511.921875, 511.98828125, 511.88671875, 511.95703125, 512.02734375, 511.91796875]], 'v1.2': [[54.57, 53.83, 62.11, 53.83, 54.33, 53.77, 57.79, 58.77, 55.81, 55.82], [502.85546875, 502.85546875, 502.8984375, 502.91015625, 502.6953125, 502.8984375, 502.82421875, 502.89453125, 502.89453125, 502.859375]], 'v1.3': [[57.91, 49.42, 52.75, 50.58, 56.88, 49.22, 53.74, 55.14, 50.09, 49.02], [68.2578125, 68.25, 68.19921875, 68.00390625, 68.19921875, 67.98828125, 68.19921875, 68.21875, 67.984375, 67.98828125]], 'v1.4': [[48.61, 50.44, 49.96, 52.0, 48.93, 51.59, 50.88, 51.35, 52.43, 53.56], [72.7421875, 72.78125, 72.8515625, 72.72265625, 72.796875, 72.78515625, 72.76171875, 72.7578125, 72.8046875, 72.8515625]], 'v1.5': [[42.44, 42.01, 41.43, 40.94, 48.06, 41.3, 40.88, 44.07, 47.88, 39.66], [735.125, 735.33984375, 735.23828125, 735.1015625, 735.34765625, 735.3515625, 735.34375, 735.20703125, 735.26953125, 735.484375]], 'v1.6': [[16.17, 16.07, 16.08, 16.21, 16.0, 15.94, 16.15, 16.12, 16.12, 16.58], [462.75390625, 462.671875, 462.72265625, 462.75390625, 462.91015625, 462.7578125, 462.8359375, 462.68359375, 462.66796875, 462.8046875]], 'v1.7': [[22.31, 22.23, 21.99, 22.2, 21.98, 22.17, 21.95, 22.17, 21.87, 22.12], [463.99609375, 464.09765625, 463.9609375, 464.0625, 463.9296875, 463.875, 464.0234375, 463.9296875, 463.9921875, 463.91796875]], 'v1.8': [[17.94, 18.13, 17.95, 17.96, 17.88, 17.88, 17.98, 17.87, 17.97, 17.97], [463.046875, 462.94921875, 462.9453125, 463.2265625, 463.21875, 463.10546875, 463.06640625, 462.94921875, 462.87890625, 462.98046875]], 'v1.9': [[16.51, 16.5, 16.35, 16.73, 16.38, 16.38, 16.56, 16.51, 16.43, 16.41], [462.046875, 461.94140625, 462.03515625, 462.109375, 462.15234375, 462.1171875, 462.03125, 462.046875, 461.91796875, 462.0703125]], 'v1.10': [[20.24, 20.16, 20.36, 20.32, 20.34, 20.55, 20.2, 20.3, 20.2, 20.21], [464.01953125, 463.98046875, 463.91015625, 463.8828125, 463.984375, 464.03515625, 464.015625, 463.98046875, 464.07421875, 464.02734375]], 'v1.11': [[20.19, 20.18, 20.25, 20.34, 20.2, 20.19, 20.19, 20.41, 20.2, 20.23], [463.88671875, 464.1796875, 464.1171875, 463.96484375, 464.17578125, 464.05078125, 463.90625, 463.91796875, 463.94921875, 463.81640625]], 'v2.0': [[13.1, 12.61, 12.46, 12.47, 12.48, 12.39, 12.35, 12.4, 12.4, 12.48], [84.3125, 84.296875, 84.33984375, 84.05078125, 84.1875, 84.1328125, 84.1875, 84.2578125, 84.15625, 84.34375]]}




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

