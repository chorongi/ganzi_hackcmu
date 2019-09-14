from tkinter import *
from PIL import Image,ImageTk
import random
import numpy as np
import cv2
import sys
import time
import math
import collections
import coloredlogs, logging
sys.setrecursionlimit(10000)
####################################
# customize these functions
####################################


def init(data):
    data.isGameStart = False
    data.isHelp = False
    data.helpX = data.width*1/13
    data.helpY = data.height*1/13
    data.carWidth = 25
    data.carHeight = 50
    data.cursorX = 0
    data.cursorY = 0
    data.helpFont = None
    data.helpColor = "white"
    data.backX = data.width*1/13
    data.backY = data.height*1/13
    data.backFont = None
    data.nameFont = None
    data.nameColor = None
    data.lineColor = "beige"
    data.isSelectedCar = None
    data.useMotion = True
    data.position = 0
    data.isReady = False
    data.carX, data.carY = data.width/2, data.height/2
    data.binary = None
    
def mouseMotion(event, data):
    data.cursorX, data.cursorY = event.x, event.y

        
def keyPressed(event, data):
    if event.keysym == "r":
        data.isReady = True
        print(data.isReady)
        
def timerFired(data):
    if data.isSelectedCar == "red":
        data.useMotion = False
        if data.redCarY < data.height and data.position==0:
            data.redCarY += 5
        elif data.redCarY > -300:
            data.position = 1
            data.redCarY-= 12
        else: data.isGameStart = True


def cursorPositionStart(canvas, data):
    return None
    

    
    
def cursorPostitionHelp(canvas, data):
    if(data.cursorX > data.backX-30 and data.cursorX < data.backX+30 and
        data.cursorY > data.backY-10 and data.cursorY < data.backY+20):
        data.backFont = "Helvetica 24 bold"
    else:
        data.backFont = "Helvetica 18 bold underline"


def opencvToTk(frame):
    """Convert an opencv image to a tkinter image, to display in canvas."""
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb_image)
    tk_image = ImageTk.PhotoImage(image=pil_img)
    return tk_image

def cameraFired(data):
    """Called whenever new camera frames are available.

    Camera frame is available in data.frame. You could, for example, blur the
    image, and then store that back in data. Then, in drawCamera, draw the
    blurred frame (or choose not to).
    """
    
    # For example, you can blur the image.
    #data.frame = cv2.GaussianBlur(data.frame, (11, 11), 0)

def drawRectOnHand(data):
    palm_area = 0;
    min_area = 10000;
    color=(0, 255, 0);
    thickness = 2;
    
    box = data.frame[105:175, 505:575]
    object_color = box
    object_color_hsv = cv2.cvtColor(object_color, cv2.COLOR_BGR2HSV)
    object_hist = cv2.calcHist([object_color_hsv], [0, 1], None,
                               [12, 15], [0, 180, 0, 256])
    hsv_frame = cv2.cvtColor(data.frame, cv2.COLOR_BGR2HSV)
    object_segment = cv2.calcBackProject(
        [hsv_frame], [0, 1], object_hist, [0, 180, 0, 256], 1)

    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    cv2.filter2D(object_segment, -1, disc, object_segment)
    _, segment_thresh = cv2.threshold(
        object_segment, 70, 255, cv2.THRESH_BINARY)
        
    kernel = None
    eroded = cv2.erode(segment_thresh, kernel, iterations=2)
    dilated = cv2.dilate(eroded, kernel, iterations=2)
    binary = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)
    _,cnt,_ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for (i, c) in enumerate(cnt):
            area = cv2.contourArea(c)
            if area > palm_area:
                palm_area = area
                flag = i
    if flag is not None and palm_area > min_area:
        cnt = cnt[flag]
        # cpy = data.frame.copy()
        cv2.drawContours(data.frame, [cnt], -2, color, thickness)
        print("hi")
        return data.frame
    else:
        print("no")
        return data.frame
        
    # for i in range(len(cnt)):
    #     x,y,w,h=cv2.boundingRect(cnt[i])
    #     if w > 100 and h > 100:
    #         cv2.rectangle(data.frame,(x,y),(x+w,y+h),(255,0,255), 2)
                
def drawCamera(canvas, data):
    _, data.frame = data.camera.read()
    data.frame = cv2.flip(data.frame,1)
    cameraFired(data)
    drawRectOnHand(data)
    data.tk_image = opencvToTk(data.frame)
    canvas.create_image(data.width/2, data.height/2, image=data.tk_image)


def redrawAll(canvas, data):
    # draw in canvas
    # if data.isGameStart == False and data.isHelp == False:
    #     cursorPositionStart(canvas, data)
    #     drawStartScreen(canvas, data)
    # elif data.isGameStart == False and data.isHelp == True:
    #     cursorPostitionHelp(canvas, data)
    #     drawHelpScreen(canvas, data)
    # elif data.isGameStart == True and data.isReady == False:
    drawCamera(canvas, data)
    # elif data.isReady == True:
    #     moveCar(data)
    #     drawCar(canvas, data)

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                 fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()   

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
        
    def mouseMotionWrapper(event, canvas, data):
        #if data.useMotion == True:
        mouseMotion(event, data)
        #redrawAllWrapper(canvas, data)
        
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.cameraIndex = 0
    camera = cv2.VideoCapture(data.cameraIndex)
    data.camera = camera
    data.timerDelay = 1 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    root.bind('<Motion>', lambda event:
                            mouseMotionWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    
    # and launch the app
    root.mainloop()  # blocks until window is closed
    data.camera.release()
    print("bye!")



if __name__ == "__main__":
    run(1000, 600)