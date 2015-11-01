# basic 4 digit LED clock program
# David Saul 2015  david@pimuxclock.co.uk

# runs under Python 3.xx
# pin usage config assums a A+,B+ or rev 2 Pi  - ie with 40 pin connector

# WARNING - this application disables python garbage collection, to slightly improve performance
# comment this out if you see randon crashes

import RPi.GPIO as GPIO         # to allow control of GPIO
import time                     # for delay timing
from time import sleep          # for delay timing

import datetime                 # for real time
from datetime import datetime   # for real time numbers

import glob                     # needed to support automatic setup of DS18B20

# try commenting these 2 lines out if you see random crashes
import gc                       # for managing garbage collection
gc.disable()                    # disable garabage collect, minimises some random dislay blips
                                # on slower Pi's

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

#------------------------------

# display 'char'[0-9 a-f] on charater 'disp' [1-4]

def dispchar(char,dispt,sec):
        
# uses simple if / else if construct
# no error handling to save time

# any segments required are first turned on  [ active low ] and all character drives disabled
# those not needed are turned off [ active high ] and the single required charater drive is enabled

        
        if char == '0':
                GPIO.output([segA,segB,segC,segD,segE,segF,segDP,char1,char2,char3,char4],GPIO.LOW)
                GPIO.output([segG,dispt],GPIO.HIGH)
        elif char == '1':
                GPIO.output([segB,segC,segDP,char1,char2,char3,char4],GPIO.LOW)
                GPIO.output([segA,segD,segE,segF,segG,dispt],GPIO.HIGH)
        elif char == '2':
                GPIO.output([segA,segB,segD,segE,segG,segDP,char1,char2,char3,char4],GPIO.LOW)
                GPIO.output([segF,segC,dispt],GPIO.HIGH)
        elif char == '3':
                GPIO.output([segA,segB,segC,segD,segG,segDP,char1,char2,char3,char4],GPIO.LOW)
                GPIO.output([segE,segF,dispt],GPIO.HIGH)
        elif char == '4':
                GPIO.output([segB,segC,segF,segG,segDP,char1,char2,char3,char4],GPIO.LOW)
                GPIO.output([segA,segD,segE,dispt],GPIO.HIGH)
        elif char == '5':
                GPIO.output([segA,segB,segC,segD,segF,segG,segDP,char1,char2,char3,char4],GPIO.LOW)
                GPIO.output([segB,segE,dispt],GPIO.HIGH)
        elif char == '6':
                GPIO.output([segA,segC,segD,segE,segF,segG,segDP,char1,char2,char3,char4],GPIO.LOW)
                GPIO.output([segB,dispt],GPIO.HIGH)
        elif char == '7':
                GPIO.output([segA,segB,segC,segDP,char1,char2,char3,char4],GPIO.LOW)
                GPIO.output([segD,segE,segF,segG,dispt],GPIO.HIGH)
        elif char == '8':
                GPIO.output([segA,segB,segC,segD,segE,segF,segG,segDP,char1,char2,char3,char4],GPIO.LOW)
                GPIO.output([dispt],GPIO.HIGH)
        elif char == '9':
                GPIO.output([segA,segB,segC,segD,segF,segG,segDP,char1,char2,char3,char4],GPIO.LOW)
                GPIO.output([segE,dispt],GPIO.HIGH)
        else:
                GPIO.output([segA,segB,segC,segD,segE,segF,segG,dispt,char1,char2,char3,char4],GPIO.LOW)


# displays a flashing centrol colon
        if sec == True and dispt == char2:

                GPIO.output(segDP,GPIO.LOW)
        else:
                GPIO.output(segDP,GPIO.HIGH)    

        return


#main

print()
print()
print(" Basic Raspberry Pi MUX Clock Application ")
print(" Python 3 Version Rev 1")
print(" Note: - this version does not implement temp sensor")
print() 
print(" hit control / C to stop ")
print()
print()

#set up display variables

muxtime = 0.005         # sets delay between each chararter display
                        # needs to be as large as possible to free up
                        # time for other resources to run
                        # it is less critical for the RPI B version 2 because of it's extra speed
bal = 0.001             # this is used to balance the 4th digit brigtness
                        # by  negating the extra time it takes to
                        # run the datetime function at the end of each display cycle

while True:

# main mux display loop

# get the time
# coment out either 12 or 24 format as required
#       time = datetime.now().strftime('%H%M%S')        #24 hour format
        time = datetime.now().strftime('%l%M%S')        #12 hour format

# logic for flashing central colon

        if int(time[5:6]) % 2 ==1:
                sec=True
        else:
                sec=False


# drive each segment inturn by calling dispchar routine

        char = time[0:1]
        dispt = char1

        dispchar(char,dispt,sec)

        sleep(muxtime)

        char = time[1:2]
        dispt = char2

        dispchar(char,dispt,sec)

        sleep(muxtime)

        char = time[2:3]
        dispt = char3

        dispchar(char,dispt,sec)

        sleep(muxtime)

        char = time[3:4]
        dispt = char4

        dispchar(char,dispt,sec)

        sleep(muxtime-bal)

