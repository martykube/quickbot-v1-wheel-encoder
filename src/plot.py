#!/usr/bin/python

import matplotlib.pyplot as plt
import time


def getData(filename):
    f = open(filename)
    times = []
    voltages = []

    for line in f:
        (time, voltage) = line.split()
        times.append(time)
        voltages.append(voltage)

    return (times, voltages)


def showData(filename, pos, xlow, xhigh, ylow, yhigh):
    plt.subplot(pos)
    (times, voltages) = getData(filename)
    plt.plot(times, voltages)
    plt.title(filename)
    plt.xlim(xlow, xhigh)
    plt.ylim(ylow, yhigh)



showData('10s-left-actual.txt', '221', 3, 5, 0, 1600)
showData('10s-left-filtered.txt', '223', 3, 5, -0.2, 1.2)
showData('10s-right-actual.txt', '222', 3, 5, 0, 1600)
showData('10s-right-filtered.txt', '224', 3, 5, -0.2, 1.2)


plt.show()

