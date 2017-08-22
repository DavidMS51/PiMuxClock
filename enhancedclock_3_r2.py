# 4 digit LED clock and temperature display program for use with PiMuxClock board
# David Saul 2015  david@pimuxclock.co.uk


# This application is coded to work with Python version 2.xx

# address of DS18B20 is automatically setup
# the application assumes only one device [ the DS18B20 ] is connected to the 1-wire bus

# WARNING - this application disables python garbage collection, to slightly improve performance
# check this if you see randon crashes

import RPi.GPIO as GPIO         # to allow control of GPIO
import time                     # for timing
from time import sleep          # for timing

import datetime                 # for real time
from datetime import datetime   # for real time numbers

import glob                     # needed to support automatic setup of DS18B20


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

# temp key

tempkey = 23

GPIO.setup(tempkey, GPIO.IN)


#------------------------------
# extra GPIO setup
# these are not used in this application but
# are set to inputs by default to reduce the risk of damage
# if you do have them connected to anything

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

# any segments required are first turn on  [ active low ] and all charater drives disabled
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
        elif char == 'C':
                GPIO.output([segA,segD,segE,segF,segDP,char1,char2,char3,char4],GPIO.LOW)
                GPIO.output([segB,segC,segG,dispt],GPIO.HIGH)
        elif char == 'F':
                GPIO.output([segA,segE,segF,segG,segDP,char1,char2,char3,char4],GPIO.LOW)
                GPIO.output([segB,segC,segD,dispt],GPIO.HIGH)
        else:
                GPIO.output([segA,segB,segC,segD,segE,segF,segG,dispt,char1,char2,char3,char4],GPIO.LOW)

# displays a flashing centrol colon
        if sec == True and dispt == char2:

                GPIO.output(segDP,GPIO.LOW)
        else:
                GPIO.output(segDP,GPIO.HIGH)    

        return

# blanks the display

def blankdsp():
        
        GPIO.output([segA,segB,segC,segD,segE,segF,segG,dispt,char1,char2,char3,char4],GPIO.LOW)
        
        return

# identify folder address for DS18B20 

def sens_add():
        
        base_dir = '/sys/bus/w1/devices/'
        
        device_folder = glob.glob(base_dir + '28*')[0]
        device_file = device_folder + '/w1_slave'
        return(device_file)

def read_temp_file(device_file):

        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines


def get_temp(id):

# get setup SPI locaton
        device_file = sens_add()
        raw_data = read_temp_file(device_file)

# check for valid reading
        while raw_data[0].find('YES') == -1:
                print ('data err')
                sleep(0.1)
                raw_data = read_temp_file(device_file)

        t_pos = raw_data[1].find('t=')

        if t_pos != -1:
                temp = raw_data[1][t_pos+2:]            # all good return temp as string

        return temp

# basic convert for temp in C to F [ assumes temp is a string ] 
# this will not work for negative values

def conv_tempctof(t1):

        t2 = int(t1)                    # first convert temp to integer
        t2 = t2 / 1000                  # scale
        t3 = ((t2 * 9) / 5 ) + 32       # then do the classic math
        t1 = str(t3)                    # back to string

# pad out string to optimise display
        if len(t1) == 1:
                t1 =t1 + "  "
        elif len(t1) == 2:
                t1 = t1 + " "

        
        return(t1)      



#main

# welcome text

print ()
print ()
print (" Raspberry Pi MUX Clock and Temperature Application ")
print (" Python 2.x Rev 1")
print (" hit control / C to stop ")
print ()
print ()

# set up display varables

muxtime = 0.005         # sets delay between each chararter display
                        # needs to be as large as possible to free up
                        # time for other resources to run

bal = 0.001             # this is used to balance the 4th digit brigtness
                        # by  negating the extra time it takes to
                        # run the datetime function at the end of each display cycle

unit = "C"              # temp unit

while True:

# check for temp key
# if yes read temp sensor and display for about 1 second

        while GPIO.input(tempkey) == 0:
                
                blankdsp()      # clear the display, this is needed as the following
                                # get_temp function is quite slow so upsets the
                                # display update

                try:
                        temp = get_temp(id)

                except:
                        temp = '000'
                
                count = 0               # time out counter
                sec = True              # decimal point handling

# uncomment the following lines to get a basis readback in Fahrenheit
#-------------------------------------------
#               temp =  conv_tempctof(temp)
#               unit = "F"
#               sec = False
#-------------------------------------------

# display temperature until count times out
# drive each segment inturn by calling dispchar routine

                while count <200:
        
                        char = temp[0:1]
                        dispt = char1

                        dispchar(char,dispt,sec)

                        sleep(muxtime)

                        char = temp[1:2]
                        dispt = char2

                        dispchar(char,dispt,sec)

                        sleep(muxtime)

                        char = temp[2:3]
                        dispt = char3

                        dispchar(char,dispt,sec)

                        sleep(muxtime)

                        char = unit
                        dispt = char4

                        dispchar(char,dispt,sec)

                        sleep(muxtime - bal)
                
                        count=count+1

# main mux display thread

# get the time
# coment out either 12 or 24 format as required

        time = datetime.now().strftime('%H%M%S')        #24 hour format
#        time = datetime.now().strftime('%l%M%S')       #12 hour format

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

        sleep(muxtime - bal)

# end
