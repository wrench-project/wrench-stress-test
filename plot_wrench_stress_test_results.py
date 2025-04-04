#!/usr/bin/env python3
import sys
import math
import ast
import statistics
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

data={'1.0': [[2.11, 1.9, 1.12, 1.04, 1.02], [5824.6953125, 5523.26953125, 5375.40625, 5233.79296875, 5119.96875]], '1.1': [[1.38, 1.19, 1.12, 1.2, 1.14], [5025.5078125, 4815.87109375, 4604.25, 4654.25390625, 4757.92578125]], '1.2': [[0.25, 0.21, 0.21, 0.21, 0.21], [5497.640625, 5523.640625, 5519.59765625, 5345.96875, 5405.765625]], '1.3': [[0.18, 0.16, 0.16, 0.16, 0.16], [120.48046875, 120.35546875, 120.5078125, 120.375, 120.5078125]], '1.4': [[0.23, 0.2, 0.2, 0.2, 0.2], [152.7421875, 152.625, 152.625, 152.703125, 152.72265625]], '1.5': [[0.27, 0.25, 0.25, 0.25, 0.25], [5597.42578125, 5248.14453125, 5004.5546875, 5194.13671875, 4952.59375]], '1.6': [[0.37, 0.32, 0.27, 0.29, 0.28], [5255.29296875, 3897.67578125, 4157.21484375, 3995.5390625, 4660.16015625]], '1.7': [[1.71, 1.57, 1.5, 1.78, 1.52], [5833.89453125, 5484.578125, 5003.66015625, 5391.03515625, 5692.2265625]], '1.8': [[1.4, 1.29, 1.09, 1.06, 1.11], [5528.35546875, 5157.02734375, 5089.10546875, 4873.515625, 5086.99609375]], '1.9': [[0.75, 0.54, 0.38, 0.42, 0.39], [5639.96875, 5484.265625, 5508.0625, 5482.21875, 5394.39453125]], '1.10': [[0.45, 0.43, 0.43, 0.42, 0.42], [5207.0859375, 4997.4375, 4971.67578125, 4648.30078125, 4692.19921875]], '1.11': [[0.53, 0.43, 0.43, 0.43, 0.44], [5418.65625, 5406.62890625, 5191.24609375, 5203.16015625, 5380.828125]], '2.0': [[0.72, 0.6, 0.59, 0.59, 0.59], [161.640625, 161.48828125, 161.53125, 161.59375, 161.48828125]], '2.1': [[0.66, 0.6, 0.61, 0.61, 0.68], [191.21484375, 191.06640625, 191.296875, 191.21484375, 191.2265625]], '2.2': [[0.68, 0.65, 0.65, 0.72, 0.65], [151.42578125, 151.421875, 151.42578125, 151.42578125, 151.421875]], '2.3': [[0.73, 0.67, 0.69, 0.67, 0.67], [181.9453125, 181.9453125, 182.11328125, 181.9453125, 182.12890625]], '2.4': [[0.66, 0.66, 0.66, 0.65, 0.64], [204.76953125, 204.68359375, 204.76953125, 204.68359375, 204.68359375]], '2.5': [[0.61, 0.56, 0.56, 0.56, 0.58], [204.8359375, 204.85546875, 204.85546875, 204.85546875, 204.84375]], '2.6': [[0.69, 0.57, 0.57, 0.62, 0.57], [204.859375, 204.859375, 204.859375, 204.859375, 204.84765625]]}













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

