#!/usr/bin/python

LOW = '0'
HIGH = '1'
state = LOW

f = open("10s-right-filtered.txt")
for line in f:
    (time, curr_state) = line.split()
    if state == LOW and curr_state == HIGH:
        print time
    state = curr_state
    
