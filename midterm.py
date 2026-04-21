

#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

import math
import yagmail

yag_mail = yagmail.SMTP(user='mayaj.lerma@gmail.com', password="hzzs tgew kztq lhwn", host='smtp.gmail.com')

To= "mayalerma@gwu.edu" # Use temp-mail.org for testing this code
Subject = "Air Quality Warning"
Body1 = ""
The temperature of the room has exceeded the safe threshold of 80 degrees Fahrenheit.
""

Body2 = ""
Unsafe levels of gas have been detected.
""
Body3 = ""
The humidity of the room has exceeded the safe threshold of 50%.
""

DHTPIN = 22
DO = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup([23,24], GPIO.OUT)
GPIO.setup (DO, GPIO.IN)

MAX_UNCHANGE_COUNT = 100

STATE_INIT_PULL_DOWN = 1
STATE_INIT_PULL_UP = 2
STATE_DATA_FIRST_PULL_DOWN = 3
STATE_DATA_PULL_UP = 4
STATE_DATA_PULL_DOWN = 5

def read_dht11_dat():
GPIO.setup(DHTPIN, GPIO.OUT)
GPIO.output(DHTPIN, GPIO.HIGH)
time.sleep(0.05)
GPIO.output(DHTPIN, GPIO.LOW)
time.sleep(0.02)
GPIO.setup(DHTPIN, GPIO.IN, GPIO.PUD_UP)

unchanged_count = 0
last = -1
data = []
while True:
current = GPIO.input(DHTPIN)
data.append(current)
if last != current:
unchanged_count = 0
last = current
else:
unchanged_count += 1
if unchanged_count > MAX_UNCHANGE_COUNT:
break

state = STATE_INIT_PULL_DOWN

lengths = []
current_length = 0

for current in data:
current_length += 1

if state == STATE_INIT_PULL_DOWN:
if current == GPIO.LOW:
state = STATE_INIT_PULL_UP
else:
continue
if state == STATE_INIT_PULL_UP:
if current == GPIO.HIGH:
state = STATE_DATA_FIRST_PULL_DOWN
else:
continue
if state == STATE_DATA_FIRST_PULL_DOWN:
if current == GPIO.LOW:
state = STATE_DATA_PULL_UP
else:
continue
if state == STATE_DATA_PULL_UP:
if current == GPIO.HIGH:
current_length = 0
state = STATE_DATA_PULL_DOWN
else:
continue
if state == STATE_DATA_PULL_DOWN:
if current == GPIO.LOW:
lengths.append(current_length)
state = STATE_DATA_PULL_UP
else:
continue
if len(lengths) != 40:
#print ("Data not good, skip")
return False

shortest_pull_up = min(lengths)
longest_pull_up = max(lengths)
halfway = (longest_pull_up + shortest_pull_up) / 2
bits = []
the_bytes = []
byte = 0

for length in lengths:
bit = 0
if length > halfway:
bit = 1
bits.append(bit)
#print ("bits: %s, length: %d" % (bits, len(bits)))
for i in range(0, len(bits)):
byte = byte << 1
if (bits[i]):
byte = byte | 1
else:
byte = byte | 0
if ((i + 1) % 8 == 0):
the_bytes.append(byte)
byte = 0
#print (the_bytes)
checksum = (the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3]) & 0xFF
if the_bytes[4] != checksum:
#print ("Data not good, skip")
return False

return the_bytes[0], the_bytes[2]

def Print(x):
if x == 1:
print ('')
print (' *********')
print (' * Safe~ *')
print (' *********')
print ('')
if x == 0:
print ('')
print (' ***************')
print (' * Danger Gas! *')
print (' ***************')
print ('')



def main():
print ("Raspberry Pi wiringPi DHT11 Temperature test program
")
status = 1
led = 0
Print(status)
count = 0
while True:

tmp = GPIO.input(DO)
if tmp != status:
Print(tmp)
status = tmp
if status == 0:
count += 1
if count % 2 == 0:
led = 0
else:
led = 1
else:
led = 0
count = 0

time.sleep(0.2)
result = read_dht11_dat()
if result:
humidity, temperature = result
print ("humidity: %s %%, Temperature: %s C" % (humidity, temperature))
if ((temperature > 30) or (humidity > 50) or (led == 1)):
GPIO.output(24, GPIO.LOW)
GPIO.output(23, GPIO.HIGH)
else:
GPIO.output(23, GPIO.LOW)
GPIO.output(24, GPIO.HIGH)
if temperature > 30:
yag_mail.send(to=To, subject=Subject, contents=Body1)
if humidity > 50:
yag_mail.send(to=To, subject=Subject, contents=Body3)
if led == 1:
yag_mail.send(to=To, subject=Subject, contents=Body2)
time.sleep(1)

def destroy():
GPIO.cleanup()

if __name__ == '__main__':
try:
main()
except KeyboardInterrupt:
destroy()

