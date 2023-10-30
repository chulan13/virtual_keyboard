#import libraries
import numpy as np
import mediapipe as mp
import cv2 
import time
import math

#create a class for hand detection
class handDetector():
    def __init__(self, mode = False, maxHands = 2, modelComplexity=1 , detectionConf = 0.5, trackConf = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionConf = detectionConf
        self.trackConf = trackConf
        self.modelComplex = modelComplexity
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex, self.detectionConf, self.trackConf)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)

        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
    
    def findPos(self, img, handNo=0, draw=True):
        self.lmList = []
        if self.result.multi_hand_landmarks:
           myhand = self.result.multi_hand_landmarks[handNo]
           for id, lm in enumerate(myhand.landmark):
                
                
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx,cy), 2, (255,0,255), cv2.FILLED)
        return self.lmList
    
    def findDistance(self, img, p1, p2, draw = True):
        x1, y1 = self.lmList[p1][1], self.lmList[p1][2]
        x2, y2 = self.lmList[p2][1], self.lmList[p2][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        if draw:
            cv2.circle(img, (x1, y1), 15, (255,0,255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255,0,255), cv2.FILLED)
            cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 3) 
            cv2.circle(img, (cx, cy), 15, (255,0,255), cv2.FILLED)


        length = math.hypot(x2-x1, y1-y2)
        print(length)
        return int(length), img, [x1, y1, x2, y2, cx, cy]
       
# test
def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)

    detector = handDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPos(img)
        if len(lmList) != 0:
            detector.findDistance(img, 9, 12)
            
            
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        
        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()
