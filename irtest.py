######################
# irtest.py 
# author: Siyao Liu
#What I do here:
#use ir beam break sensor to control picamera
#run the program
#if the ir beam is broken, camera starts
#after camera starts, press button22 to selfie, if beam is broken again, camera stops
#whenever you press button 17, the program quits
from time import sleep
import RPi.GPIO as GPIO
from picamera import PiCamera, Color

GPIO.setmode(GPIO.BCM) 
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

camera=PiCamera()
camera.rotation=180
camera.resolution=(500,500)
camera.annotate_text_size=160
camera.annotate_background=Color('green')
camera.annotate_foreground=Color('yellow')

i=0
cameraflag=False
while True:
    sleep(0.1)
    if(not GPIO.input(26)):
        cameraflag=True
        #print 'beeeeeeeeeeeeeeeee'
        print cameraflag
        print GPIO.input(26)
    while(cameraflag):
        print 'in the while loop'
        camera.start_preview(alpha=255, fullscreen=False, window=(100,100,640,480))
        while True:
            sleep(0.1)
            if(not GPIO.input(26)):
                print GPIO.input(26)
                cameraflag=False
                break
            if(not GPIO.input(22)):
                print 'Selfie %s' %i
                camera.capture('/home/pi/pro/buttoncontrol%s.jpg' %i)
                i+=1
            if(not GPIO.input(17)):
                quit()
        camera.stop_preview()
    if(not GPIO.input(17)):
        quit()
        
GPIO.cleanup()
    
