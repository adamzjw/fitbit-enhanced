__author__ = 'adamzjw'

import numpy as np
import matplotlib.pyplot as plt

class DistanceTimeSeries:
    def __init__(self, rawData):
        self.timeSeries = self._preprocess(rawData)

    def _preprocess(self, rawData):
        # to-do: detect raw data type
        rawData = rawData['activities-distance-intraday']['dataset']
        time2int = lambda x: map(int, x.split(':'))
        rawTime = [time2int(d['time']) for d in rawData]
        rawTime = [t[0]*3600 + t[1]*60 for t in rawTime]
        rawVal = [d['value'] for d in rawData]

        allVal = np.zeros(max(rawTime)+1)
        allVal[rawTime] = rawVal

        return allVal

    def generate_plot(self, filename='timeSeries.png'):
        allVal = self.timeSeries
        xmax = 60*60*24
        ymax = np.amax(allVal)

        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)
        ax1.plot(np.arange(allVal.shape[0]), allVal, color='blue')
        ax1.axhspan(ymin=0, ymax=60, xmax=xmax, facecolor='0.5', alpha=0.1, linewidth=0)
        ax1.axhspan(ymin=60, ymax=90, xmax=xmax, facecolor='0.5', alpha=0.3, linewidth=0)
        ax1.axhspan(ymin=90, ymax=140, xmax=xmax, facecolor='0.5', alpha=0.5, linewidth=0)
        ax1.axhspan(ymin=140, ymax=ymax, xmax=xmax, facecolor='0.5', alpha=0.7, linewidth=0)
        ax1.set_xlim((0, xmax))
        ax1.set_ylim((0, ymax))
        fig1.savefig(filename)

    # to-do: dump and load