# Standard port assignments for use with PiMuxClock board
# David Saul 2015  david@pimuxclock.co.uk

# compatable with python rev v2.xx and 3.xx


# This is just a code segment

import RPi.GPIO as GPIO         # to allow control of GPIO

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

# temp key

tempkey = 23

GPIO.setup(tempkey, GPIO.IN)


# extra GPIO setup

gp24 = 24
gp25 = 25
gp14 = 14
gp15 = 15

GPIO.setup([gp24,gp25], GPIO.IN)

