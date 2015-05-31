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


def showData(filename, pos):
    plt.subplot(pos)
    (times, voltages) = getData(filename)
    plt.plot(times, voltages)
    plt.title(filename)



showData('left-35.txt', '211')
showData('right-35.txt', '212')

plt.show()

