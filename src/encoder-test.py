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
PWM.start(pwmPin[LEFT], 57)
# forward
GPIO.output(dir2Pin[LEFT], GPIO.HIGH)

GPIO.setup(dir1Pin[RIGHT], GPIO.OUT)
GPIO.setup(dir2Pin[RIGHT], GPIO.OUT)
GPIO.output(dir1Pin[RIGHT], GPIO.LOW)
GPIO.output(dir2Pin[RIGHT], GPIO.LOW)
PWM.start(pwmPin[RIGHT], 75)
# forward
GPIO.output(dir2Pin[RIGHT], GPIO.HIGH)


t0 = time.time()
for loop in range(1, 300):
    for side in [LEFT, RIGHT]:
        ENC_TIME[side][ENC_IND[side]] = time.time() - t0
        ADC_LOCK.acquire()
        ENC_VAL[side][ENC_IND[side]] = ADC.read_raw(encPin[side])
        time.sleep(ADCTIME)
        ADC_LOCK.release()
        print "{0} {1} {2}".format(side, ENC_TIME[side][ENC_IND[side]], ENC_VAL[side][ENC_IND[side]])
        ENC_IND[side] = (ENC_IND[side] + 1) % ENC_BUF_SIZE

GPIO.output(dir1Pin[LEFT], GPIO.LOW)
GPIO.output(dir2Pin[LEFT], GPIO.LOW)
GPIO.output(dir1Pin[RIGHT], GPIO.LOW)
GPIO.output(dir2Pin[RIGHT], GPIO.LOW)
PWM.set_duty_cycle(pwmPin[LEFT], 0)
PWM.set_duty_cycle(pwmPin[RIGHT], 0)
PWM.stop(pwmPin[LEFT])
PWM.stop(pwmPin[RIGHT])
PWM.cleanup()


