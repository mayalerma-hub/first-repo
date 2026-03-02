#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import math

DO = 13
GPIO.setmode(GPIO.BCM)

def setup():
    GPIO.setup      (DO,    GPIO.IN)
    GPIO.setup      ([23,24,  GPIO.OUT)

def Print(x):
    if x == 1:
        print ('')
        print ('   *********')
        print ('   * Safe~ *')
        print ('   *********')
        print ('')
    if x == 0:
        print ('')
        print ('   ***************')
        print ('   * Danger Gas! *')
        print ('   ***************')
        print ('')

def loop():
    status = 1
    count = 0
    while True:

        tmp = GPIO.input(DO)
        if tmp != status:
            Print(tmp)
            status = tmp
        if status == 0:
            count += 1
            if count % 2 == 0:
                GPIO.output(23, GPIO.LOW)
                GPIO.output(24, GPIO.HIGH)
            else:
                GPIO.output(24, GPIO.LOW)
                GPIO.output(23, GPIO.HIGH)
        else:
            GPIO.output(23, GPIO.LOW)
            GPIO.output(24, GPIO.HIGH)
            count = 0

        time.sleep(0.2)

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        destroy()
