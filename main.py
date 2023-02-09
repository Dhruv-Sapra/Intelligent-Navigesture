import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np

puckPos = [100, 100]
speedX = 5
speedY = 5
gameOver = False
score = [0, 0]


Background = cv2.imread(r"C:\\Users\\LEGION\Desktop\\AllDesktop\\Inheritance\\Ping Pong Game\\4729668.png",cv2.IMREAD_UNCHANGED)
Background = cv2.resize(Background, (1280,720))
PaddleLeft = cv2.imread(r"C:\\Users\\LEGION\\Desktop\\AllDesktop\\Inheritance\\Ping Pong Game\\unnamed.png",cv2.IMREAD_UNCHANGED)
PaddleLeft =cv2.resize(PaddleLeft,(100,100))
PaddleRight = cv2.imread(r"C:\\Users\\LEGION\\Desktop\\AllDesktop\\Inheritance\\Ping Pong Game\\unnamed.png",cv2.IMREAD_UNCHANGED)
PaddleRight =cv2.resize(PaddleRight,(100,100))
Puck =cv2.imread(r"C:\Users\LEGION\Desktop\AllDesktop\Inheritance\Ping Pong Game\share-it-green-glowing-circle-11563079981sivw5upspu.png",cv2.IMREAD_UNCHANGED)
Puck =cv2.resize(Puck,(80,80))


detector = HandDetector(detectionCon=0.8,maxHands=2)

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

while True:
    success, img = cap.read()

    img = cv2.flip(img, 1)
    imgRaw = img.copy()
 
    hands, img = detector.findHands(img, flipType=False) 
    img = cv2.addWeighted(img, 0, Background, 1, 0)
    
    if hands:
        for hand in hands:
            x, y, w, h = hand['bbox']
            h1, w1, _ = PaddleLeft.shape
            y1 = y - h1 // 2
            y1 = np.clip(y1, 101, 415)
            x1 = x - w1 // 2
            x1 = np.clip(x1, 20, 500)


            h2, w2, random = PaddleRight.shape
            y2 = y - h2//2
            y2 = np.clip(y2, 101, 415)
            x2 = x - w1//2
            x2 = np.clip(x2,700,1200)
            
 
            if hand['type'] == "Left":
                img = cvzone.overlayPNG(img, PaddleLeft, (x1, y1))
                if x1-w1//2 < puckPos[0] < x1 + w1//2 and y1-h1//2 < puckPos[1] < y1 + h1//2:
                    speedX = -speedX
                    speedX +=5
                    puckPos[0] += 25
                    score[0] += 1

            if hand['type'] == "Right":
                img = cvzone.overlayPNG(img, PaddleRight, (x2, y2))
                if x2-w2//2 < puckPos[0] < x2 +w2//2 and y2-h2//2 < puckPos[1] < y2 + h2//2:
                    speedX = -speedX
                    speedX -= 5
                    puckPos[0] -= 25
                    score[1] += 1

    if puckPos[1] >= 1400 or puckPos[1] <= 80:
        speedY = -speedY
 
    # puckPos[0] += speedX
    # puckPos[1] += speedY

    if puckPos[0] < 81 or puckPos[0] > 1100:
        gameOver = True
 
    if gameOver:
        imgGameOver = cv2.imread(r"C:\Users\LEGION\Desktop\AllDesktop\Inheritance\Ping Pong Game\gameOver.png")
        imgGameOver = cv2.resize(imgGameOver, (1280,720))
        img = imgGameOver
        # cv2.putText(img, str(score[1] + score[0]).zfill(2), (585, 360), cv2.FONT_HERSHEY_COMPLEX,
        #             2.5, (200, 0, 200), 5)
 
    # If game not over move the ball
    else:
 
        # Move the Ball
        if puckPos[1] >= 500 or puckPos[1] <= 10:
            speedY = -speedY
 
        puckPos[0] += speedX
        puckPos[1] += speedY
 
        # Draw the ball
        img = cvzone.overlayPNG(img, Puck, puckPos)
 
        cv2.putText(img, str(score[0]), (300, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
        cv2.putText(img, str(score[1]), (900, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
 
    cv2.putText(img, str(score[0]), (300, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
    cv2.putText(img, str(score[1]), (900, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('r'):
        puckPos = [100, 100]
        speedX = 5
        speedY = 5
        gameOver = False
        score = [0, 0]
        img = Background
        
