#!/usr/bin/python

import time
import threading
import numpy as np
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.ADC as ADC


LEFT = 1
RIGHT = 0
encPin=('P9_37', 'P9_39')
ADCTIME = 0.001
ADC_LOCK = threading.Lock()

## Encoder buffer constants and variables
ENC_BUF_SIZE = 2**9
ENC_IND = [0, 0]
ENC_TIME = [[0]*ENC_BUF_SIZE, [0]*ENC_BUF_SIZE]
ENC_VAL = [[0]*ENC_BUF_SIZE, [0]*ENC_BUF_SIZE]

ADC.setup()

# Power to wheels
(LEFT, RIGHT)
dir1Pin = ('P8_14', 'P8_12')
dir2Pin = ('P8_16', 'P8_10')
pwmPin = ('P9_16', 'P9_14')
pwm = 0

GPIO.setup(dir1Pin[LEFT], GPIO.OUT)
GPIO.setup(dir2Pin[LEFT], GPIO.OUT)
GPIO.output(dir1Pin[LEFT], GPIO.LOW)
GPIO.output(dir2Pin[LEFT], GPIO.LOW)
PWM.start(pwmPin[LEFT], 58)
# forward
GPIO.output(dir2Pin[LEFT], GPIO.HIGH)

GPIO.setup(dir1Pin[RIGHT], GPIO.OUT)
GPIO.setup(dir2Pin[RIGHT], GPIO.OUT)
GPIO.output(dir1Pin[RIGHT], GPIO.LOW)
GPIO.output(dir2Pin[RIGHT], GPIO.LOW)
PWM.start(pwmPin[RIGHT], 79)
# forward
GPIO.output(dir2Pin[RIGHT], GPIO.HIGH)

# Schmitt filter.  
# Transitions from low to high state at v_trasition + v_max
# Transitions from high to low state at v_trasition - v_min
v_transition = 800.0
v_max = 300.0
v_min = 300.0
HIGH = 1
LOW = 0
state = LOW

run_duration_seconds = 20

t0 = time.time()
while (time.time() - t0) < run_duration_seconds:
    for side in [LEFT, RIGHT]:
        # acquire encoder reading
        ADC_LOCK.acquire()
        elapsed_time = time.time() - t0
        voltage = ADC.read_raw(encPin[side])
        ADC_LOCK.release()
        # run through filter
        voltage = float(voltage)
        if state == LOW and (voltage > (v_transition + v_max)):
            state = HIGH
        elif state == HIGH and (voltage < (v_transition - v_min)):
            state = LOW
        print "{0} {1} {2} {3}".format(side, elapsed_time, voltage, state)
        time.sleep(ADCTIME)


GPIO.output(dir1Pin[LEFT], GPIO.LOW)
GPIO.output(dir2Pin[LEFT], GPIO.LOW)
GPIO.output(dir1Pin[RIGHT], GPIO.LOW)
GPIO.output(dir2Pin[RIGHT], GPIO.LOW)
PWM.set_duty_cycle(pwmPin[LEFT], 0)
PWM.set_duty_cycle(pwmPin[RIGHT], 0)
PWM.stop(pwmPin[LEFT])
PWM.stop(pwmPin[RIGHT])
PWM.cleanup()


