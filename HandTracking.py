import cv2
import mediapipe as mp


class handTracking:

    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):

        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, 1, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLandMarks in self.results.multi_hand_landmarks:

                if draw:
                    self.mpDraw.draw_landmarks(img, handLandMarks, self.mpHands.HAND_CONNECTIONS)

        return img

    def findLocation(self, img, handNo=0, draw=True):

        lmList = []

        if self.results.multi_hand_landmarks:
            self.myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(self.myHand.landmark):

                h, w, c = img.shape
                cx, cy, cz = int(lm.x * w), int(lm.y * h), lm.z
                lmList.append([id, cx, cy, cz])

                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 255, 255), cv2.FILLED)

        return lmList


def main():

    # Filler code ############################################
    cap = cv2.VideoCapture(0)
    handTrack = handTracking()

    while True:

        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = handTrack.findHands(img)
        lmList = handTrack.findLocation(img)

        if len(lmList) != 0:
            print(lmList[4])

        cv2.imshow("Video Capture", img)
        cv2.waitKey(1)


if __name__ == '__main__':

    main()