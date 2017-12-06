##########################################
# image.py
# Author: Siyao Liu & Junyi Huang
# load image from RPi3
# show a image on the middle of a window
# use button to expand or shrink the size of an image
##########################################


from time import sleep
import RPi.GPIO as GPIO
from PIL import Image
import pygame

GPIO.setmode(GPIO.BCM) 
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pygame.init()

size =width, height = 800,800
black = 0,0,0
winstyle = 0 # | FULLSCREEN
screen = pygame.display.set_mode(size, winstyle,32)
img=pygame.image.load('buttoncontrol5.jpg').convert()
i=0
j=0
while True:
    (x,y)=img.get_rect().size
    screen.fill(black)
    screen.blit(img,((800-x)/2,(800-y)/2))
    pygame.display.flip()
    if (not GPIO.input(17)):
        quit()
    if (not GPIO.input(22)):
        i+=1
        #img=pygame.transform.smoothscale(img,(x+10*i,y+10*i))
        img=pygame.transform.rotozoom(img,0.0,1.1)
    if (not GPIO.input(23)):
        j+=1
        #img=pygame.transform.smoothscale(img,(x-10*i,y-10*i))
        img=pygame.transform.rotozoom(img,0.0,0.9)

GPIO.cleanup()