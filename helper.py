import numpy as np
import matplotlib.pyplot as plt

def generate_plot(ts, filename='timeSeries.png'):
        xmax = ts.shape[0]
        ymax = np.amax(ts)

        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)
        ax1.plot(np.arange(ts.shape[0]), ts, color='blue')
        ax1.axhspan(ymin=0, ymax=60, xmax=xmax, facecolor='0.5', alpha=0.1, linewidth=0)
        ax1.axhspan(ymin=60, ymax=90, xmax=xmax, facecolor='0.5', alpha=0.3, linewidth=0)
        ax1.axhspan(ymin=90, ymax=140, xmax=xmax, facecolor='0.5', alpha=0.5, linewidth=0)
        ax1.axhspan(ymin=140, ymax=ymax, xmax=xmax, facecolor='0.5', alpha=0.7, linewidth=0)
        ax1.set_xlim((0, xmax))
        ax1.set_ylim((0, ymax))
        #fig1.savefig(filename)

def fill_na(ts):
    repeat_cnt = 0
    for i in xrange(ts.shape[0]):
        if ts[i] == 0:
            if repeat_cnt < 30 and i > 4:
                ts[i] = np.mean(ts[i-5:i-1])
                repeat_cnt += 1
        else:
            repeat_cnt = 0
    return ts