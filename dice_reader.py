import cv2
import numpy as np
import time
import serial
import random
import math
import pygame
import sys
import RPi.GPIO as GPIO
from pygame.locals import *
from utilities import *
from cv2_functions import *
from business_hours import *
last_message_time = 0
demo_mode = False
x = None
y = None
num_dice = 3
cap = cv2.VideoCapture(0)               # '0' is the webcam's ID. usually it is 0 or 1. 'cap' is the video object.
cap.set(5, -4)                         # '5' references video's brightness. '-4' sets the brightness.
file = open('random.txt', 'a')
counter = 0                             # script will use a counter to handle FPS.
readings = [0, 0]                       # lists are used to track the number of pips.
display = [0, 0]
#arduino serial port
ser = serial.Serial(port='/dev/ttyACM0',baudrate = 9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)
#distance to move cam view over
cam_offset = 720
pygame.init()
pygame.display.set_caption("Dice Reader")
title_font = pygame.font.Font('Roboto-Regular.ttf' , 60)
dice_font = pygame.font.Font('dice.ttf', 200)
info_font = pygame.font.Font('Roboto-Regular.ttf' , 35)
results_font = pygame.font.Font('Roboto-Regular.ttf' , 55)
screen = pygame.display.set_mode([1360,768])
msg = []
rolls = []
lastDigits = []
BLUE=(0,0,255)
TEAL=(24,188,156)
WHITE=(200,200,200)
NAVY=(50,50,100)
RED=(255,0,0)
ORANGE=(255,147,53)
#demo toggle pin
pin = 18
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
try:
    while True:
        if counter >= 90000:                # set maximum sizes for variables and lists to save memory.
            counter = 0
            readings = [0, 0]
            display = [0, 0]
     
        ret, im = cap.read()                                    # 'im' will be a frame from the video.
        detector = get_detector()
        keypoints = detector.detect(im)                         # keypoints is a list containing the detected blobs.
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = frame.swapaxes(0,1)
        frame = pygame.surfarray.make_surface(frame)
        screen.fill(TEAL)#
        screen.blit(frame, (cam_offset,0))
        for keypoint in keypoints:
            pygame.draw.circle(screen,NAVY,(int(keypoint.pt[0]+cam_offset),int(keypoint.pt[1])), 7)
        reading = len(keypoints)                                # 'reading' counts the number of keypoints (pips).
        readings.append(reading)                            # note the reading from this frame.
 
        if readings[-1] == readings[-2] == readings[-3]:    # if the last 3 readings are the same...
            display.append(readings[-1])                    # ... then we have a valid reading.
 
        # if the most recent valid reading has changed, and it's something other than zero, then proceed.
        

         
        if display[-1] > 1 and display[-1] == len(keypoints):
            if time.time()-last_message_time > 2: #don't spam digits
                demo_mode = GPIO.input(pin)                
                msg = ["THE RANDOMIZER"]
                if not class_now() or demo_mode:
                    if(ser.isOpen()): #Tell the arduino to start the motor
                        ser.write("1")
                    msg.extend(get_info_lines(np.floor(time.time()/15)%4))
                    
                    msg.append('')
                    
                    #CLUSTERING
                    Z = []
                    for keypoint in keypoints:
                        Z.append([keypoint.pt[0], keypoint.pt[1]])
                    Z = np.float32(Z)
                    
                    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
                    try:
                        ret,label,center=cv2.kmeans(Z,num_dice,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
                    except:
                        msg.append('Clustering error!')
                        msg.append('Rerolling...')
                    # Now separate the data
                    rolls = []
                    for i in range(num_dice):
                        rolls.append(len(Z[label.ravel()==i])) # Note the flatten()
                        roll = rolls[-1];
                        #append the formula for counting the base 10
                        senary_msg = ''#'TO BASE-6: ((' + str(roll) + ' - 1) * 6^' + str(i) + ') / 2) = ' + str(((roll-1)*6**i)/2)  
                        #msg.append( "ROLL" + str(i+1) + ":     " + senary_msg)
                        msg.append("")
                    decimal = convert_to_decimal(rolls[2], rolls[1], rolls[0])
                    msg.append("RANDOM DIGITS: " + str(decimal))
                    if len(str(decimal)) ==2 :
                        lastDigits.insert(0, str(decimal))
                    if len(lastDigits) > 10:
                        lastDigits.pop(10)
                   
                    if len(decimal) == 2:
                        with open("random.txt", "a") as myfile:
                            myfile.write(str(decimal))
                    msg.extend(get_stat_lines(lastDigits))
                    
                    last_message_time = time.time()
                    readings = [0, 0]
                else:
                    msg.extend(get_info_lines(99)) #99 is the code for closed message
                    msg.extend(get_stat_lines(lastDigits))
#                try:
#                    myData = ser.readline()
#                    if myData == "1":
#                        demo_mode = True
#                    else:
#                        demo_mode = False
#                except:
#                    print "error reading serial data from arduino"
        
        counter += 1
        label = []
        colors = [
            RED,
            NAVY,
            NAVY,
            NAVY,
            NAVY,
            NAVY,
            NAVY,
            NAVY,
            NAVY,
            NAVY,
            NAVY,
            NAVY,
            NAVY,
            NAVY,
            NAVY,
            NAVY,
            NAVY
            ]
        for line in range(len(msg)):
            if line == 0:
                font = title_font
            elif line < 6:
                font = info_font
            else:
                font = results_font
            label.append(font.render(msg[line], True, colors[line]))
        for line in range(len(label)):
            if line == 0:
                offset_y = 0
                spacing = 35
            elif line < 6:
                offset_y = 30
                spacing = 35
            else:
                offset_y = -50
                spacing = 55
            screen.blit(label[line],(10,offset_y+spacing*line))
        label = []
        if not class_now():
            for roll in rolls:
                label.append(dice_font.render(str(roll), True, NAVY))
            for line in range(len(label)):
                screen.blit(label[line],(50 + line * 200,250) )
                base6str = rolls[line]-1
                base6str *= 6**(2-line)
                base6str /= 2
                base6str = str(int(np.floor(base6str)))
                base6 = info_font.render(base6str, True, NAVY)
                screen.blit(base6,(150 + line * 200,450) )
        pygame.display.update()
        k = cv2.waitKey(30) & 0xff                              # press [Esc] to exit.
        if k == 27:
            break
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
              sys.exit(0)

except KeyboardInterrupt,SystemExit:
    pygame.quit()
    cv2.destroyAllWindows()

 
cv2.destroyAllWindows()                                     # since we exited the loop above, end the script.
 
