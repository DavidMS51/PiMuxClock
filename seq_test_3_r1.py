# basic messy sequence test for PiMuxClock board
# application simply runs though each charater on each digit
# use simply to confirm everything is connected ok

#David Saul 2015  david@pimuxclock.co.uk

# runs under Python 3.xx
# pin usage config assums a A+,B+ or rev 2 Pi  - ie with 40 pin connector


import RPi.GPIO as GPIO         # to allow control of GPIO
import time                     # for delay timing
from time import sleep          # for delay timing

import datetime                 # for real time
from datetime import datetime   # for real time numbers



#define GPIO pin usage  - BCM numbering assumed throughout

GPIO.setmode(GPIO.BCM)

#turn off warning
GPIO.setwarnings(False)


#segments

segA = 5
segB = 6
segC = 13
segD = 19
segE = 26
segF = 12
segG = 16
segDP = 20

GPIO.setup([segA,segB,segC,segD,segE,segF,segG,segDP], GPIO.OUT)

#Characters   [ left to right view display from front ] 

char1 = 17
char2 = 27
char3 = 22
char4 = 18

GPIO.setup([char1,char2,char3,char4], GPIO.OUT)

#------------------------------
# extended GPIO setup

# temp key

tempkey = 23

GPIO.setup(tempkey, GPIO.IN)

# extra GPIO connections

# these are setup to default to inputs to reduce the risk of
# damage if you inadvertanly leave them being driven

gp24 = 24
gp25 = 25
gp14 = 14
gp15 = 15

GPIO.setup([gp14,gp15,gp24,gp25], GPIO.IN)

#main

print()
print()
print(" Basic Raspberry Pi MUX Clock Test Application ")
print(" Python 3.x Rev 1")
print()
print()
print(" hit control / C to stop ")
print()
print()


d = .15                         # seq speed
char_sel = [char1,char2,char3,char4]    # char codes    

while True:
        c = 0                   # tmp counter
        while c < 4:

                dispt = char_sel[c]

                GPIO.output([segA,segB,segC,segD,segE,segF,segDP,char1,char2,char3,char4],GPIO.LOW)
                GPIO.output([segG,dispt],GPIO.HIGH)
                sleep(d)
                GPIO.output([segB,segC,segDP,char1,char2,char3,char4],GPIO.LOW)
                GPIO.output([segA,segD,segE,segF,segG,dispt],GPIO.HIGH)
                sleep(d)
                GPIO.output([segA,segB,segD,segE,segG,segDP,char1,char2,char3,char4],GPIO.LOW)
                GPIO.output([segF,segC,dispt],GPIO.HIGH)
                sleep(d)
                GPIO.output([segA,segB,segC,segD,segG,segDP,char1,char2,char3,char4],GPIO.LOW)
                GPIO.output([segE,segF,dispt],GPIO.HIGH)
                sleep(d)
                GPIO.output([segB,segC,segF,segG,segDP,char1,char2,char3,char4],GPIO.LOW)
                GPIO.output([segA,segD,segE,dispt],GPIO.HIGH)
                sleep(d)
                GPIO.output([segA,segB,segC,segD,segF,segG,segDP,char1,char2,char3,char4],GPIO.LOW)
                GPIO.output([segB,segE,dispt],GPIO.HIGH)
                sleep(d)
                GPIO.output([segA,segC,segD,segE,segF,segG,segDP,char1,char2,char3,char4],GPIO.LOW)
                GPIO.output([segB,dispt],GPIO.HIGH)
                sleep(d)
                GPIO.output([segA,segB,segC,segDP,char1,char2,char3,char4],GPIO.LOW)
                GPIO.output([segD,segE,segF,segG,dispt],GPIO.HIGH)
                sleep(d)
                GPIO.output([segA,segB,segC,segD,segE,segF,segG,segDP,char1,char2,char3,char4],GPIO.LOW)
                GPIO.output([dispt],GPIO.HIGH)
                sleep(d)
                GPIO.output([segA,segB,segC,segD,segF,segG,segDP,char1,char2,char3,char4],GPIO.LOW)
                GPIO.output([segE,dispt],GPIO.HIGH)
                sleep(d)

                c = c + 1
