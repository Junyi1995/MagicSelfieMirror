################################################################################
# Magic Selfie Mirror V4.0
# Author Junyi Huang (jh2635) & Siyao Liu (sl2928)
# Major Updates: Adding "resize on", "resize off" and "quit" icon in photo booth
# Mode switches by gestures 
# More sensitive gestures detection
################################################################################

# import library
import time
import RPi.GPIO as GPIO
from PIL import Image
import sys
import Adafruit_DHT
from picamera import PiCamera, Color
import pygame
# setting GPIO
GPIO.setmode(GPIO.BCM) 
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
pygame.init()
# Setting size of monitor
size = width, height = 1280, 1024   
winstyle = pygame.FULLSCREEN
black = 0,0,0
white = 255,255,255
screen = pygame.display.set_mode(size,winstyle,32)
# setting flags and counters 
A = False
timecount = 0
count6 = 0
count10 = 0
timeflag = True
gtcount = 0
gtflag = True
dhtcount = 0
dhtflag = True
cameraflag = False
resizeflag = True
cameracount = 0
camera=PiCamera()
camera.resolution = (1000, 900)
cameralogo=pygame.image.load('cameralogo.png')
cameralogo = pygame.transform.rotozoom(cameralogo,0.0,0.1)
cameralogorect = cameralogo.get_rect()
cameralogorect.center = (100,900)
#camera.brightness=70
camera.contrast=30
camera.rotation=180
camera.hflip = True
##camera=PiCamera()
##camerastartflag False

# defination of functions
# encoder of up-down side
def encoder1():
    return 8*GPIO.input(26)+4*GPIO.input(19)+2*GPIO.input(13)+GPIO.input(6)
# encoder of right-left side
def encoder2():
    return 8*GPIO.input(12)+4*GPIO.input(16)+2*GPIO.input(20)+GPIO.input(21)
# time information
def Time(timeflag):
    if timeflag:
        # setting font of time
        my_font= pygame.font.SysFont('roboto',40, bold = True)
        # set dictionary of time information
        timenow={'Date':(120,130), 'Time':(340,130), time.ctime(time.time()) : (250,200)}
        for my_text, text_pos in timenow.items():
            text_surface=my_font.render(my_text, True, white)
            rect=text_surface.get_rect(center=text_pos)
            screen.blit(text_surface, rect)
# displaying greeting in homepage
def Greeting(gtflag):
    if gtflag:
        my_font= pygame.font.SysFont('roboto',100, bold = True)
        # setting font of greeting
        greeting={'Hi, there!' : (500,550)}
        for my_text, text_pos in greeting.items():
            text_surface=my_font.render(my_text, True, white)
            rect=text_surface.get_rect(center=text_pos)
            screen.blit(text_surface, rect)
# humidity and temperature information
def Humidity(dhtflag,humidity, temperature):
    if dhtflag:
        my_font= pygame.font.SysFont('roboto',40, bold = True)
        #timenow={'Date':(120,130), 'Time':(340,130), time.ctime(time.time()) : (250,200)}
        humidity={'Temp: {0:0.1f}C'.format(temperature):(800,130), 'Humidity: {0:0.1f}%'.format(humidity): (800,200)}
        for my_text, text_pos in humidity.items():
            text_surface=my_font.render(my_text, True, white)
            rect=text_surface.get_rect(center=text_pos)
            screen.blit(text_surface, rect)
# define quitbutton phrase
def quitbutton():
    my_font= pygame.font.SysFont('roboto',30, bold = False)
    quitbutton={'Quit' : (450,950)}
    for my_text, text_pos in quitbutton.items():
        text_surface=my_font.render(my_text, True, white)
        rect=text_surface.get_rect(center=text_pos)
        screen.blit(text_surface, rect)
# define resizeoff phrase
def resizeoff(resizeflag):
    if(resizeflag == True):
        my_font= pygame.font.SysFont('roboto',30)
        text_surface=my_font.render('resize off' , True, white)
        rect=text_surface.get_rect(center=(800,950))
        screen.blit(text_surface, rect)
# define queue to store left and right position of detected gestures
def leftright():
    ud = [0,0,0]
    lr = [0,0,0]
    timestart = time.time()
    # update position every 0.2 secondes
    while time.time() - timestart < 0.2:
        time.sleep(0.09)
        if(encoder1() > 0):
            ud.insert(0,encoder1()) # update new position 
            ud.pop()
            if(ud[1] > ud[0]):
                print ud
                ud = [0,0,0]
                print "left slide signal"
                return 1
            if(ud[2] < ud[1] and ud[1] < ud[0]):
                print ud
                ud = [0,0,0]
                print "right slide signal"
                return 2
# define expand function in picture preview mode, scale factor according 
def expand(img,factor):
    img=pygame.transform.rotozoom(img,0.0,factor*0.1 + 1)
# define shrink function 
def shrink(img, factor):
    img=pygame.transform.rotozoom(img,0.0,1 - factor*0.1)
# define camera mode and picture preview mode
def Secondmode(cameraflag):
        if(cameraflag):
            screen.fill(black)
            # define filters
            imgeffect=('none','oilpaint','sketch','hatch','negative','gpen','cartoon','emboss')
            # turn on the camera
            camera.start_preview(alpha=255, fullscreen=False, window=(0,0,1000,900))
            # displaying quitbutton at the bottom 
            quitbutton()
            # refresh the page
            pygame.display.flip()
            i = 1
            j = 0
            picprevcount = 0
            count6 = 0
            count10 = 0
            while True:
                print(encoder1(), encoder2())
                # using bottom beam sensor reciever 6 to control quit
                if(encoder1() == 6):
                    count6+=1
                    print count6
                # if detect left slide, change to next filter
                if(leftright() == 1):
                    j+=1
                    camera.image_effect=imgeffect[j % 8]
                # if detect right slide, change to previous filter
                if(leftright() == 2):
                    j-=1
                    camera.image_effect=imgeffect[j % 8]       
                # take a picture by pressing GPIO 22
                if (not GPIO.input(22)):
                    # take picture and save it
                    camera.capture('/home/pi/pro/pictures/%s.jpg' %i)
                    # create a small preview of latest picture in right bottom 
                    img=pygame.image.load('/home/pi/pro/pictures/%s.jpg' %i).convert()                    
                    img=pygame.transform.smoothscale(img,(90,90))
                    imgrect = img.get_rect()
                    imgrect.center = (950,950)
                    screen.blit(img, imgrect)
                    quitbutton()
                    pygame.display.flip()
                    i+=1
                # entering picutre preview mode by gesture on right bottom
                if(encoder2() == 10 and i > 1):
                        picprevcount+=1
                        if(picprevcount >= 3):
                            resizeflag = True
                            picprevcount = 0
                            camera.stop_preview()
                            screen.fill(black)
                            picnum = i - 1
                            piclast = pygame.image.load('/home/pi/pro/pictures/%s.jpg' %picnum).convert()
                            piclastrect = piclast.get_rect()
                            picsize = piclast.get_rect().size
                            picsize0 = piclast.get_rect().size
                            # keep the picture in the center of the mirror
                            piclastrect.center = (500,450)
                            screen.blit(piclast, piclastrect)
                            quitbutton()
                            resizeoff(resizeflag)
                            pygame.display.flip()
                            while True:
                                print(encoder1(), encoder2())
                                if(encoder1() == 6):
                                    count6+=1
                                    print count6
                                # using rightslide to preview the previous picture
                                if(picnum>1 and leftright() == 2):
                                    picnum -=1
                                    piclast = pygame.image.load('/home/pi/pro/pictures/%s.jpg' %picnum).convert()
                                    
                                    piclastrect = piclast.get_rect()
                                    picsize = piclast.get_rect().size
                                    picsize0 = piclast.get_rect().size
                                    piclastrect.center = (500,450)
                                    screen.fill(black)
                                    screen.blit(piclast, piclastrect)
                                    quitbutton()
                                    resizeoff(resizeflag)
                                    pygame.display.flip()
                                # using leftslide to view the next picture
                                if(picnum<(i-1) and leftright() == 1):
                                    picnum +=1
                                    piclast = pygame.image.load('/home/pi/pro/pictures/%s.jpg' %picnum).convert()
                                    piclastrect = piclast.get_rect()
                                    picsize = piclast.get_rect().size
                                    picsize0 = piclast.get_rect().size
                                    piclastrect.center = (500,450)
                                    screen.fill(black)
                                    screen.blit(piclast, piclastrect)
                                    quitbutton()
                                    resizeoff(resizeflag)
                                    pygame.display.flip()
                                if(encoder2() == 10):
                                    count10 +=1
                                # gesture in right bottom to enter resize mode
                                if(not GPIO.input(23) or count10 > 3):
                                    count10 = 0
                                    first = [0,0]
                                    second = [0,0]
                                    resizeflag = False
                                    screen.fill(black)
                                    screen.blit(piclast, piclastrect)
                                    quitbutton()
                                    resizeoff(resizeflag)
                                    pygame.display.flip()
                                    while True:
                                        print(encoder1(), encoder2())
                                        if(encoder1() == 6):
                                            count6+=1
                                            print count6
                                        # enter resize mode
                                        my_font= pygame.font.SysFont('roboto',30)
                                        text_surface=my_font.render('resize on' , True, white)
                                        rect=text_surface.get_rect(center=(800,950))
                                        screen.blit(text_surface, rect)
                                        quitbutton()
                                        resizeoff(resizeflag)
                                        pygame.display.flip()
                                        time.sleep(0)
                                        # record the gesture scale
                                        second = first
                                        first = [encoder1(), encoder2()]
                                        print first + second
                                        if(second[0] != 0 and second[1] != 0 and first[0] != 0 and first[1] != 0):
                                            r = (first[0] + first[1] - second[0] - second[1] + 0.0)/(second[0] + second[1] + 0.0)
                                            picsize = [picsize[0] * (r + 1),picsize[1] * (r + 1)]
                                            r1 = (0.0 + picsize[0] + picsize[1])/(0.0 + picsize0[0] + picsize0[1])
                                            print r1
                                            picshow= pygame.image.load('/home/pi/pro/pictures/%s.jpg' %picnum).convert()
                                            # expand or shrink picture according to the scale of gesture
                                            picshow = pygame.transform.rotozoom(picshow,0.0,r1)
                                            picshowrect = picshow.get_rect()
                                            picshowrect.center = (500,450)
                                            screen.fill(black)
                                            screen.blit(picshow, picshowrect)
                                            quitbutton()
                                            pygame.display.flip()
                                        # quit resize mode by quit gesture and button connecting GPIO 17
                                        if ((not GPIO.input(17)) or (count6 >= 7)):
                                            resizeflag = True
                                            count6 = 0
                                            screen.fill(black)
                                            screen.blit(piclast, piclastrect)
                                            quitbutton()
                                            resizeoff(resizeflag)
                                            pygame.display.flip()
                                            break
                                    time.sleep(0.3)
                                # quit picture preview mode by quit gesture and physical button 17
                                if(not GPIO.input(17)) or (count6 >= 3):
                                    count6 = 0
                                    screen.fill(black)
                                    break
                            # turn on camera again
                            camera.start_preview(alpha=255, fullscreen=False, window=(0,0,1000,900))
                            screen.blit(img, imgrect)
                            quitbutton()
                            pygame.display.flip()
                            time.sleep(0.3)
                # quit camera mode and return to home page 
                if ( not GPIO.input(17)) or (count6 >= 3):
                    count6 = 0
                    camera.stop_preview()
                    cameraflag = not cameraflag
                    time.sleep(0.5)
                    break
                #quit()
                
        
        
humidity,temperature=Adafruit_DHT.read_retry(11,4)
while True:      
    if encoder2() != 0:
        A = True
        time.sleep(0.5)
        break
while A:
    # using flags to control displaying or disappearing of the information
    screen.fill(black)
    Time(timeflag)
    Greeting(gtflag)
    Humidity(dhtflag,humidity, temperature)
    screen.blit(cameralogo, cameralogorect)
    pygame.display.flip()
    time.sleep(0.001)
    print(encoder1(), encoder2())
    # left up to control the date message
    if encoder1() == 1 or encoder1() == 2 or encoder1() == 3 or encoder1() == 4:
        timecount+=1
        if timecount > 3:
            time.sleep(0.4)
            timecount = 0
            timeflag = not timeflag
            screen.blit(cameralogo, cameralogorect)
            pygame.display.flip()
    # mid bottom to control the greetings
    if encoder1() == 5 or encoder1() == 6 or encoder1() == 7:
        gtcount+=1
        if gtcount > 3:
            time.sleep(0.3)
            gtcount=0
            gtflag=not gtflag
            screen.blit(cameralogo, cameralogorect)
            pygame.display.flip()
    # right up to control the temperatrue and humidity
    if encoder1() == 8 or encoder1() == 9 or encoder1() == 10 or encoder1() == 11:
        dhtcount+=1
        if dhtcount > 4:
            time.sleep(0.2)
            dhtcount=0
            dhtflag=not dhtflag
            screen.blit(cameralogo, cameralogorect)
            pygame.display.flip()
        #if camerastartflag == False: use flag to start and shutdown camera
        #camera.start_preview(alpha=100) # alpha is used to set transparent level
    # camera icon in the left bottom, control entering camera mode
    if encoder2() == 11:
        cameracount+=1
        if cameracount > 5:
            time.sleep(0.3)
            cameracount=0
            cameraflag=not cameraflag
            Secondmode(cameraflag)
            screen.fill(black)
            timeflag = True
            gtflag = True
            dhtflag = True
            #pygame.display.flip()             
    if(not GPIO.input(17)):
        quit()
GPIO.cleanup()



