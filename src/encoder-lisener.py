#!/usr/bin/python

import os
import socket

import time
import numpy as np
import matplotlib.pyplot as plt
import threading


# open a socket and listen for UDP packets
#import numpy as np
#import sys
#import signal
#import time
#import threading


TELEMETRY_PORT=5006
QB_ROBOT_IP =  os.getenv('QB_ROBOT_IP', '192.160.1.160')
QB_BASE_IP =  os.getenv('QB_BASE_IP', '192.160.1.169')



print "Robot: {0}:{1}".format(QB_ROBOT_IP, TELEMETRY_PORT)
print "Base : {0}:{1}".format(QB_BASE_IP, TELEMETRY_PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(False)
sock.bind((QB_BASE_IP, TELEMETRY_PORT))


BUFFER_SIZE = 10
BUFFER_INDEX = 0
BUFFER_MUTEX = threading.Lock()
BUFFER_TIME = np.zeros(BUFFER_SIZE, dtype=float)
BUFFER_ENC_LEFT = np.zeros(BUFFER_SIZE, dtype=float)
BUFFER_ENC_RIGHT = np.zeros(BUFFER_SIZE, dtype=float)

def poll():
    global BUFFER_SIZE
    global BUFFER_INDEX
    global BUFFER_MUTEX
    global BUFFER_TIME
    global BUFFER_ENC_LEFT
    global BUFFER_ENC_RIGHT
    while True:
        try:
            print 'Polling'
            data = sock.recv(2048)
            print data
            data = data.strip()
            (str_l, str_r) = data[1:-1].split(',')
            left = float(str_l)
            right = float(str_r)
            timestamp = time.time()
            BUFFER_MUTEX.acquire()
            print 'Buffering {0} {1} {2}'.format(timestamp, left, right)
            BUFFER_TIME[BUFFER_INDEX] = timestamp
            BUFFER_ENC_LEFT[BUFFER_INDEX] = left
            BUFFER_ENC_RIGHT[BUFFER_INDEX] = right
            BUFFER_INDEX = (BUFFER_INDEX + 1) % BUFFER_SIZE
            BUFFER_MUTEX.release()
        except socket.error as mesg:
            pass
        time.sleep(0.1)


def readBuffer():
    global BUFFER_SIZE
    global BUFFER_INDEX
    global BUFFER_MUTEX
    global BUFFER_TIME
    global BUFFER_ENC_LEFT
    global BUFFER_ENC_RIGHT
    global t0
    index = 0
    time_data = np.empty(BUFFER_SIZE, dtype=float)
    left_data = np.empty(BUFFER_SIZE, dtype=float)
    right_data = np.empty(BUFFER_SIZE, dtype=float)
    BUFFER_MUTEX.acquire()
    while index < BUFFER_SIZE:
        time_data[index] = BUFFER_TIME[(BUFFER_INDEX + index) % BUFFER_SIZE] - t0
        left_data[index] = BUFFER_ENC_LEFT[(BUFFER_INDEX + index) % BUFFER_SIZE]
        right_data[index] = BUFFER_ENC_RIGHT[(BUFFER_INDEX + index) % BUFFER_SIZE]
        index = index + 1
    BUFFER_MUTEX.release()
    return (time_data, left_data, right_data)
    

t0 = time.time()
(times, left, right) = readBuffer()
t = threading.Thread(target=poll)
t.setDaemon(True)
t.start()

# plotting

figure = plt.figure()
axes = figure.add_subplot(111)
axes.set_xlim(0, 10)
axes.set_ylim(0, 1500)
lines, = axes.plot(times, left)
figure.canvas.draw()
plt.show(block = False)

while True:
    print 'Yo!'
    time.sleep(2)
    (times, left, right) = readBuffer()
    print times
    print left
    lines.set_ydata(left)
    figure.canvas.draw()


# plt.ion()
# plt.show()

# for i in range(1000):
#     y = np.random.random()
#     plt.scatter(i, y)
#     plt.draw()
#     time.sleep(0.05)
