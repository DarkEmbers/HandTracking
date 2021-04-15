import cv2
import HandTracking as hT
import math
import numpy as np
from pynput.mouse import Button, Controller
import pyautogui
import time

# Initial Params ######################################################################################################

mouse = Controller()
cap = cv2.VideoCapture(0)
screenW, screenH = pyautogui.size()
screenCX, screenCY = screenW / 2, screenH / 2
tracker = hT.handTracking(maxHands=1, detectionCon=0.5, trackCon=0.5)
isPressed = False
IsInteracting = False
distanceToInteract = 25
distanceToInteract2 = 30
PlotDataX = []
PlotDataY = []

#######################################################################################################################

while True:

    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = tracker.findHands(img)

    camH, camW, camC = img.shape
    imgCX, imgCY = camW / 2, camH / 2
    scaleFactor = (screenW * screenH) / (camW * camH)
    scaleFactor *= 1.3

    lmList = tracker.findLocation(img, draw=False)
    if lmList:

        # Calculate mouse position ####################################################################################

        x1, y1, z1 = lmList[4][1], lmList[4][2], lmList[4][3]  # get thumb tip x and y and z coordinates
        x2, y2, z2 = lmList[8][1], lmList[8][2], lmList[8][3]  # get index finger tip x and y and z coordinates
        cx1, cy1 = (x1 + x2) // 2, (y1 + y2) // 2  # get midpoint coordinates of thumb and index finger
        indexThumbLength = math.hypot((x2 - x1), (y2 - y1))  # get length between index finger and thumb
        x3, y3, z3 = lmList[12][1], lmList[12][2], lmList[12][3]  # get middle finger tip x and y and z coordinates
        cx2, cy2 = (x1 + x3) // 2, (y1 + y3) // 2  # get midpoint coordinates of thumb and index finger
        middleThumbLength = math.hypot((x3 - x1), (y3 - y1))

        # Set mouse position

        xLengthScaled = (cx1 - imgCX) * scaleFactor
        yLengthScaled = (cy1 - imgCY) * scaleFactor
        endPointX = screenCX + xLengthScaled
        endPointY = screenCY + yLengthScaled
        mouse.position = (endPointX, endPointY)

        # Controls ####################################################################################################

        # index finger and thumb tap/press for left click/grab

        if (indexThumbLength <= distanceToInteract) and (not isPressed):
            t1 = time.time()
            isPressed = True

        # Check whether it's click or press

        currentTime = time.time()

        try:
            if ((currentTime - t1) <= 0.5) and isPressed:
                if indexThumbLength > distanceToInteract:
                    mouse.click(Button.left)
                    isPressed = False

            elif (currentTime - t1 > 0.5) and isPressed:
                if (indexThumbLength <= distanceToInteract) and (not IsInteracting):
                    mouse.press(Button.left)
                    IsInteracting = True

                else:
                    mouse.release(Button.left)
                    isPressed = False
                    IsInteracting = False

        except:
            pass

        # middle finger and thumb tap for right click

        if middleThumbLength <= distanceToInteract2:
            mouse.click(Button.right)

        # Visual effects ##############################################################################################

        # Index finger and thumb

        cv2.circle(img, (x1, y1), 10, (255, 255, 255), cv2.FILLED)  # draw circle at tip of thumb
        cv2.circle(img, (x2, y2), 10, (255, 255, 255), cv2.FILLED)  # draw circle at tip of index finger
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)  # draw line joining index finger and thumb
        cv2.circle(img, (cx1, cy1), 10, (255, 255, 255), cv2.FILLED)  # draw circle at midpoint of line

        if indexThumbLength <= distanceToInteract:
            cv2.circle(img, (cx1, cy1), 10, (0, 255, 0), cv2.FILLED)  # Emulate left button press

        # Middle finger and thumb

        cv2.circle(img, (x3, y3), 10, (255, 255, 255), cv2.FILLED)  # draw circle at tip of middle finger
        cv2.line(img, (x3, y3), (x1, y1), (255, 0, 0), 3)  # draw line joining middle finger and thumb
        cv2.circle(img, (cx2, cy2), 10, (255, 255, 255), cv2.FILLED)  # draw circle at midpoint of line

        if middleThumbLength <= distanceToInteract:
            cv2.circle(img, (cx2, cy2), 10, (0, 255, 0), cv2.FILLED)  # Emulate right button press

        ###############################################################################################################

    else:
        isPressed = False
        IsInteracting = False

    # cv2.imshow("Video Capture", img)
    cv2.waitKey(1)
