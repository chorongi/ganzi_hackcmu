import os
import requests
from io import BytesIO
from PIL import Image, ImageDraw
import numpy as np
import cv2
from random import randint
from handy import *




# ##############################################
# ######## get faces from test file#############
# ##############################################

raiseHeight = 160
faceWidth = 150
faceHeight = faceWidth
resize = 2


hist = captureHistogram(0)

cap = cv2.VideoCapture(0)

success,image = cap.read()

count = 0

font = cv2.FONT_HERSHEY_PLAIN
capWidth  = int(cap.get(3))
capHeight = int(cap.get(4))



while(success):
    # if pressed q break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # Capture frame-by-frame
    success, image = cap.read()
    success, image, countours, defects = detectHand(image, hist, sketchContours = True, computeDefects = True)
    fingertips = extractFingertips(defects, countours, 50, right = True)

    image = cv2.line(image, (0, raiseHeight), (int(capWidth - 1), raiseHeight), (255, 255, 255), 1)
    #saving a face
    if type(countours) == np.ndarray:
        h = countours[0][0][1]
        w = int(countours[0][0][0])
        if h < raiseHeight:
            topRightX = max(w - faceWidth, 0)
            crop_image = image[raiseHeight: raiseHeight + faceHeight, topRightX: w]
    #drawing on the frame
            image = cv2.putText(image, "Raised!", (topRightX, raiseHeight), font, 3, (0, 0, 255), 2, cv2.LINE_AA)
            image = cv2.rectangle(image, (topRightX, raiseHeight + 1), (w, raiseHeight + faceHeight), (255, 0, 255), 1)        
            

            #############################################
            ############Create test image ###############
            #############################################

            


#Close video file or capturing device
cap.release()
cv2.destroyAllWindows()

