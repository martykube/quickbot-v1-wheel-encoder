#!/usr/bin/python

file = open('left-35.txt')

# Schmitt filter.  
# Transitions to high state at v_trasition + v_max
# Transitions to low state at v_trasition - v_min
v_transition = 700
v_max = 300
v_min = 300

HIGH = 1
LOW = 0
state = LOW

for line in file:
    (time, voltage) = line.split()
    voltage = float(voltage)
    if state == LOW and (voltage > (v_transition + v_max)):
        state = HIGH
        print "{0} {1}".format(time, state)
    elif state == HIGH and (voltage < (v_transition - v_min)):
        state = LOW

