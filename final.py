#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import yagmail

yag_mail = yagmail.SMTP(user='mayaj.lerma@gmail.com', password="hzzs tgew kztq lhwn", host='smtp.gmail.com')

To= "mayalerma@gwu.edu"
Subject = "INTRUDER ALERT"
Body1 = """
WARNING: INTRUDER DETECTED!
"""

DO = 5
GPIO.setmode(GPIO.BCM)

LedPin = 17 # pin11
BuzzerPin = 22

def setup():
    GPIO.setup(DO, GPIO.IN)
    GPIO.setup(LedPin, GPIO.OUT) # Set LedPin's mode is output
    GPIO.output(LedPin, GPIO.HIGH) # Set LedPin high(+3.3V) to off led
    GPIO.setup(BuzzerPin, GPIO.OUT)
    GPIO.output(BuzzerPin, GPIO.HIGH)

def on():
    GPIO.output(BuzzerPin, GPIO.LOW)

def off():
    GPIO.output(BuzzerPin, GPIO.HIGH)

def loop():
    while True:
    laser = GPIO.input(DO)
    print ('Value: ', laser)
    #'...Laser on'
    GPIO.output(LedPin, GPIO.LOW) # led on
    time.sleep(0.5)
    if (laser == 1):
        yag_mail.send(to=To, subject=Subject, contents=Body1)
        on()
    else:
        off()

def destroy():
    GPIO.output(LedPin, GPIO.HIGH) # led off
    GPIO.cleanup() # Release resource

if __name__ == '__main__': # Program start from here
    setup()
try:
    loop()
except KeyboardInterrupt: # When 'Ctrl+C' is pressed, the child program destroy() will be executed.
    destroy()
