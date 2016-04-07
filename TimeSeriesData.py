__author__ = 'adamzjw'

import numpy as np
import matplotlib.pyplot as plt

# 1-day intra-day data container
class TimeSeriesData:
    def __init__(self):
        self.heartrate = None
        self.distance = None
        self.steps = None

    def _preprocess(self, rawData, dataLable, detail_level):
        # to-do: detect raw data type

        # convert time into real-number
        rawData = rawData[dataLable]['dataset']
        time2int = lambda x: map(int, x.split(':'))
        rawTime = [time2int(d['time']) for d in rawData]

        if detail_level == "1sec":
            rawTime = [t[0]*3600 + t[1]*60 + t[2] for t in rawTime]
        elif detail_level == "1min":
            rawTime = [t[0]*60 + t[1] for t in rawTime]
        else:
            detail_level_choices = ["1sec", "1min"]
            raise ValueError("Choices for detail_level: %s" % ",".join(detail_level_choices))

        rawVal = [d['value'] for d in rawData]

        # create value array
        ts = np.zeros(max(rawTime)+1)
        ts[rawTime] = rawVal

        return ts

    def import_heartrate_sec(self, rawData):
        ts = self._preprocess(rawData, "activities-heart-intraday", "1sec")

        # fill missing data
        repeat_cnt = 0
        for i in xrange(ts.shape[0]):
            if ts[i] == 0:
                if repeat_cnt < 300:
                    ts[i] = ts[i-1]
                    repeat_cnt += 1
            else:
                repeat_cnt = 0

        # calculate the convolution
        filt = np.ones(60)/60.0
        self.heartrate = np.convolve(filt, ts, mode='same')

    def import_heartrate_min(self, rawData):
        ts = self._preprocess(rawData, "activities-heart-intraday", "1min")
        self.heartrate = ts

    def import_distance_min(self, rawData):
        self.distance = self._preprocess(rawData, "activities-distance-intraday", "1min")

    def import_steps_min(self, rawData):
        self.steps = self._preprocess(rawData, "activities-steps-intraday", "1min")

    def _generate_plot(self, ts, filename='timeSeries.png'):
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
        fig1.savefig(filename)

    def saveAll(self, date):
        if self.heartrate is not None:
            np.save("./data/heartrate%s" % date, self.heartrate)
        if self.distance is not None:
            np.save("./data/distance%s" % date, self.distance)
        if self.steps is not None:
            np.save("./data/steps%s" % date, self.steps)

    # to-do: dump and load