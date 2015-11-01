# 4 digit LED processor temp display using PiMuxClock
# David Saul 2015 david@pimuxclock.co.uk

# coded to run on Python version 3.xx 

# pin usage config assums a A+,B+ or rev 2 Pi  - ie with 40 pin connector

# WARNING - this application disables python garbage collection, to slightly improve performance
# check this if you see randon crashes

import RPi.GPIO as GPIO         # to allow control of GPIO
import time                     # for timing
from time import sleep          # for timing

import datetime                 # for real time
from datetime import datetime   # for real time numbers



import gc                       # for managing garbage collection
gc.disable()                    # disable garabage collect, minimises some random dislay blips

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
# these are not used in this application but
# are set to inputs by default to reduce the risk of damage
# if you do have them connected to anything

# temp key

tempkey = 23

GPIO.setup(tempkey, GPIO.IN)

# extra GPIO setup


gp24 = 24
gp25 = 25
gp14 = 14
gp15 = 15

GPIO.setup([gp24,gp25], GPIO.IN)

#------------------------------



# display 'char'[0-9 a-f] on charater 'disp' [1-4]

def dispchar(char,dispt,sec):
        
# uses simple if / else if construct
# no error handling to save time

# any segments required are first turn on  [ active low ] and all charater drives disapled
# those not needed are turn off [ active high ] and the single required charater drive is enabled

        
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
        elif char == 'C':
                GPIO.output([segA,segD,segE,segF,segDP,char1,char2,char3,char4],GPIO.LOW)
                GPIO.output([segB,segC,segG,dispt],GPIO.HIGH)
        elif char == 'o':       
                GPIO.output([segA,segB,segF,segG,segDP,char1,char2,char3,char4],GPIO.LOW)
                GPIO.output([segC,segD,segE,dispt],GPIO.HIGH)
        elif char == 'F':
                GPIO.output([segA,segE,segF,segG,segDP,char1,char2,char3,char4],GPIO.LOW)
                GPIO.output([segB,segC,segD,dispt],GPIO.HIGH)
        else:
                GPIO.output([segA,segB,segC,segD,segE,segF,segG,dispt,char1,char2,char3,char4],GPIO.LOW)


        GPIO.output(segDP,GPIO.HIGH)    # force DP to always be on

        return

# basic convert for temp in C to F [ assumes temp is a string ] 
# this will not work for negative values

def conv_tempctof(t1):

        t2 = int(t1)                    # first convert temp to integer
        t3 = ((t2 * 9) / 5 ) + 32       # then do the classic math
        t1 = str(t3)                    # back to string

# pad out string to optimise display
        if len(t1) == 1:
                t1 =t1 + "  "
        elif len(t1) == 2:
                t1 = t1 + " "


        return(t1)


#main

print()
print()
print(" Raspberry Pi MUX Clock Application ")
print() 
print(" displays Pi processor temp and nothing else ")
print(" python 3.xx version")
print()
print(" hit control / C to stop ")
print()
print()

#muxdisp()      # start clock

muxtime = 0.005         # sets delay between each chararter display
                        # needs to be as large as possible to free up
                        # time for other resources to run

count = 1000            # temp update timer  - setting to 1000 to get initial value
countup = 1000          # sets how often temp is update - 1000 equates to about 25sec

sec = True              # dummy value to all use of common subroutine

unit = 'C'              # temp unit


while True:

# main mux display loop
# update the processor temp
        if count == countup:
                temp=str(round(int(open('/sys/class/thermal/thermal_zone0/temp').read()) /1e3,0))
                count = 0
                
# uncomment the following lines to get a basis readback in Fahrenheit
#-------------------------------------------
#                tt = float(temp)                # format temp to match existing
#                temp = str(int(tt))             # conversion routine
#                temp =  conv_tempctof(temp)
#                unit = 'F'
#                sec = False
#-------------------------------------------


        count = count +1


# drive each segment inturn by calling dispchar routine

        char = temp[0:1]
        dispt = char1

        dispchar(char,dispt,sec)

        sleep(muxtime)

        char = temp[1:2]
        dispt = char2

        dispchar(char,dispt,sec)

        sleep(muxtime)

        if unit == 'C':
                char = 'o'
        else:
                char = temp[2:3]

        dispt = char3
        dispchar(char,dispt,sec)

        sleep(muxtime)

        char = unit
        dispt = char4

        dispchar(char,dispt,sec)

        sleep(muxtime)

