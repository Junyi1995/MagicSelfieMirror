##########################
# testinput.py
# Author: Junyi Huang 
# test input from the beam sensor
# print out the hand position's right down corner point
##########################
import RPi.GPIO as GPIO
import time
import pygame
GPIO.setmode(GPIO.BCM) 
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# encoder1 is connected to up-down side sensors, the output of encoder1 are connected
# to GPIO 26, 19, 13, 6
def encoder1():
    return 8*GPIO.input(26)+4*GPIO.input(19)+2*GPIO.input(13)+GPIO.input(6)
# encoder1 is connected to up-down side sensors, the output of encoder1 are connected
# to GPIO 12, 16, 20, 21
def encoder2():
    return 8*GPIO.input(12)+4*GPIO.input(16)+2*GPIO.input(20)+GPIO.input(21)
while True:
    time.sleep(0.1)
    # print out the coordinate of the right down point of gesture
    input = (encoder1(), encoder2())
##    if encoder1() > 1 and encoder2():
##        print "signal"
    print input
    if(not GPIO.input(17)):
        quit()
GPIO.cleanup() 
    
