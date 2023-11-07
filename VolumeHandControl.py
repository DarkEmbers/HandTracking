import cv2
import numpy as np
import HandTracking as ht
import math
import subprocess
from pyvolume import pyvolume
import time

# Params ##############################################################################################################
cap = cv2.VideoCapture(0)
tracker = ht.handTracking(maxHands=2, detectionCon=0.7, trackCon=0.7)

#######################################################################################################################


def main():

    isTrigger1On = False
    isTrigger2On = False

    while True:

        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = tracker.findHands(img)
        cx1,cy1,cx2,cy2 = 0,0,0,0

        # Find Landmarks on Hand 1 ####################################################################################
        try:
            lmList = tracker.findLocation(img, draw=False, handNo=0)
            if len(lmList) != 0:
                isTrigger1On, cx1, cy1 = handInfo(lmList, img)

        except:
            isTrigger1On = False
            continue

        # Find Landmarks on Hand 2 ####################################################################################
        try:
            lmList = tracker.findLocation(img, draw=False, handNo=1)
            if len(lmList) != 0:
                isTrigger2On, cx2, cy2 = handInfo(lmList, img)

        except:
            isTrigger2On = False
            continue

        # Volume control ##############################################################################################
        # try:
        # Check if Index finger is tapping with Thumb and change volume ###############################################
        if isTrigger1On and isTrigger2On:
            cv2.line(img, (cx1, cy1), (cx2, cy2), (255, 0, 0), 3)
            indexThumbLength = math.hypot((cx2 - cx1), (cy2 - cy1))
            vol = np.interp(indexThumbLength, [50, 300], [0, 100])

            # Change volume ###############################################################################################
            pyvolume(level = vol)

        # except:
            # pass

        ###############################################################################################################

        cv2.imshow("Video Capture", img)
        cv2.waitKey(1)

        time.sleep(0.01)


def handInfo(lmList, img):

    # Get Location of thumb, index finger and middle finger on hand ###################################################
    x1, y1, z1 = lmList[4][1], lmList[4][2], lmList[4][3]  # get thumb tip x and y and z coords
    x2, y2, z2 = lmList[8][1], lmList[8][2], lmList[8][3]  # get index finger tip x and y and z coords
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # get index finger and thumb midpoint coords

    # Visual effects ##################################################################################################
    # cv2.circle(img, (x1, y1), 10, (255, 255, 255), cv2.FILLED)  # draw circle at tip of thumb
    # cv2.circle(img, (x2, y2), 10, (255, 255, 255), cv2.FILLED)  # draw circle at tip of index finger
    # cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)  # draw line joining index finger and thumb
    # cv2.circle(img, (cx, cy), 10, (255, 255, 255), cv2.FILLED)  # draw circle at midpoint of line

    # Calculate length of lines #######################################################################################
    length = math.hypot((x2 - x1), (y2 - y1))

    # Whether to activate hand or not #################################################################################
    if length <= 30:
        cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)  # draw circle at midpoint of line
        return True, cx, cy

    else:
        return False, cx, cy

    ###################################################################################################################


if __name__ == '__main__':
    main()
