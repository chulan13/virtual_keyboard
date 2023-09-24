import cv2
from handmodule import handDetector
import time
from pynput.keyboard import Controller


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = handDetector(detectionConf=0.8)

finalText = ''

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

keyboard = Controller()

def drawAll(img, buttonList):
    for b in buttonList:
        x,y = b.pos
        w,h = b.size
        cv2.rectangle(img, b.pos, (x+w, y+h), (255,0,255), cv2.FILLED)
        cv2.putText(img, b.text, (x+20, y+75), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 4)
    return img

class Button():
    def __init__(self, pos, text, size=[85,85]):
        self.pos = pos
        self.text = text
        self.size = size

    
    
buttonList = []


for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100*j+50, 100 * i +50], key))


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPos(img)
    img = drawAll(img, buttonList) 
    if lmList:
        for b in buttonList:
            x,y = b.pos
            w,h = b.size
            if x<lmList[8][1]<x+w and y<lmList[8][2]<y+h:
                cv2.rectangle(img, b.pos, (x+w, y+h), (175,0,175), cv2.FILLED)
                cv2.putText(img, b.text, (x+20, y+75), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 4)
                
                l = detector.findDistance(img, 12, 8)
                print(l)
                if l[0] <= 40:
                    keyboard.press(b.text)
                    cv2.rectangle(img, b.pos, (x+w, y+h), (0,255,0), cv2.FILLED)
                    cv2.putText(img, b.text, (x+20, y+75), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 4)

                    finalText += b.text
                    time.sleep(0.5)


    cv2.rectangle(img, (50, 350), (700, 450), (175, 0 , 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 425), cv2.FONT_HERSHEY_PLAIN, 5, (0,255,0), 5)

                     


                

    cv2.imshow("Image", img)
    cv2.waitKey(1)
