import cv2
import numpy as np
import Handtrackingmodule as htm
import time
import pyautogui
import mediapipe
import webbrowser


wCam, hCam = 640, 480
frameReduction = 100
smoothening = 3

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(maxHands=1,detectionCon=0.7)

wScr, hScr = pyautogui.size()


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist, bbox = detector.findPosition(img)

    if len(lmlist) != 0:
        x1, y1 = lmlist[8][1:]
        x2, y2 = lmlist[12][1:]

        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameReduction, frameReduction), (wCam - frameReduction, hCam - frameReduction),
                      (255, 0, 255), 2)

        # MOVING MODE
        if fingers[1] == 1 and fingers[2] == 0 and fingers[3]==0:
            x3 = np.interp(
                x1, (frameReduction, wCam-frameReduction), (0, wScr))
            y3 = np.interp(
                y1, (frameReduction, hCam-frameReduction), (0, hScr))

            # Smoothening
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            pyautogui.moveTo(wScr-clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # LEFT CLICK
        if fingers[1]==1 and fingers[2] == 1 and fingers[3]==0 :
            length, img, lineInfo = detector.findDistance(8, 12, img)
            print(length)
            if length < 55:
                cv2.circle(img, (lineInfo[4], lineInfo[5]),
                           15, (0, 255, 0), cv2.FILLED)
                pyautogui.click()

        # RIGHT CLICK
        if fingers[1]==0 and fingers[2] == 1 and fingers[3]==1  :
            length, img, lineInfo = detector.findDistance(12, 16, img)
            print(length)
            if length < 55:
                cv2.circle(img, (lineInfo[4], lineInfo[5]),
                           15, (0, 255, 0), cv2.FILLED)
                pyautogui.click(button= "right" )

          # SCROLL
        if fingers[0]==1 and fingers[1] == 0 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0 :
            pyautogui.scroll(-50)
        if fingers[0]==1 and fingers[1] == 1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==1 :
            pyautogui.scroll(50) 
        
         


          #webbrowser module 
        if fingers[0]==1 and fingers[1] == 1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==0 :
            webbrowser.open('https://www.google.com')
            time.sleep(0.5)
        
        
        
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (20, 50),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
