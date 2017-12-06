#######################
# dhttest.py
# connecting temperature and humidity sensor into RPi3
# read the temperature and humidity from the sensor
#######################
from time import sleep
import sys
import Adafruit_DHT
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) 
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    sleep(0.2)
    humidity,temperature = Adafruit_DHT.read_retry(11,4)
    #print(humidity, temperature)
    print'Temp: {0:0.1f}C  Humidity: {1:0.1f}%'.format(temperature,humidity)
    if (not GPIO.input(17)):
        quit()
        
GPIO.cleanup()