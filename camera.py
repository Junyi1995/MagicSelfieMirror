###########################
# camera.py
# Author: Siyao Liu
# connect Picamera into RPi3 and turn on the camera
# try different filters in Picamera
# take pictures
############################


from picamera import PiCamera, Color
from time import sleep
import RPi.GPIO as GPIO
# set up GPIO
GPIO.setmode(GPIO.BCM) 
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def encoder1():
    return 8*GPIO.input(26)+4*GPIO.input(19)+2*GPIO.input(13)+GPIO.input(6)
# create a instance of Picamera
camera=PiCamera()
# rotate camera 180 degree
camera.rotation=180
##camera.framerate=15
# preview window size
camera.resolution=(500,1100)
camera.annotate_text_size=160
camera.annotate_background=Color('green')
camera.annotate_foreground=Color('yellow')

camera.start_preview(alpha=255, fullscreen=False, window=(0,0,500,1100))
sleep(3)
# different for loops are using different filters or change different settings
for i in range (5): # from selfie0 to selfie4
    sleep(3)
    camera.capture('/home/pi/pro/selfie%s.jpg' %i) #1600x1200 1.2MB

# take a video
camera.start_recording('/home/pi/pro/firstvideo.h264') # video
sleep(5)
camera.stop_recording()

##for i in range (100): %change brightness and annotate
##    camera.annotate_text="Brightness: %s" %i
##    camera.brightness=i
##    sleep(0.1)
    
##for i in range (50):  #change contrast and annotate
##    camera.annotate_text="Contrast: %s" %i
##    camera.contrast=i
##    sleep(0.1)

##camera.annotate_text="Hi there!" #annotate
##sleep(3)
##camera.capture('/home/pi/pro/selfie_max.jpg') #1600x1200 1.2MB

##camera.image_effect='watercolor' #different effect
##sleep(5)
##camera.capture('/home/pi/pro/deinterlace2.jpg')
##
##camera.awb_mode='tungsten'
##sleep(3)
##camera.capture('/home/pi/pro/tungsten.jpg')
##
##camera.exposure_mode='night' #exposure mode
##sleep(3)
##camera.capture('/home/pi/pro/night.jpg')
##
i=1
while True:
    if ( not GPIO.input(17)):
        camera.capture('/home/pi/pro/buttoncontrol%s.jpg' %i)
        i+=1
        quit()
        
    if ( not GPIO.input(22) or encoder1()== 5):
        camera.stop_preview()
        #quit()

camera.stop_preview()
GPIO.cleanup() 