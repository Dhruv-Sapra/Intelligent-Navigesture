import cv2
import time
import numpy as np
import Handtrackingmodule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7, maxHands=1)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None
)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

vol = 0
volBar = 400
volPer = 0
area = 0

smoothness = 10  # reduce resolution to make smoother

while True:
    success, img = cap.read()

    img = detector.findHands(img)
    lmlist, bbox = detector.findPosition(img, draw=True)
    if len(lmlist) != 0:
        area = (bbox[2]-bbox[0])*(bbox[3]-bbox[1]) // 100

        if 250 < area < 1000:
            length, img, lineInfo = detector.findDistance(4, 8, img)
            volBar = np.interp(length, [50, 300], [400, 150])
            volPer = np.interp(length, [50, 300], [0, 100])

            volPer = smoothness*round(volPer/smoothness)

            fingers = detector.fingersUp()

            if  fingers[4]==0 :
                volume.SetMasterVolumeLevelScalar(volPer/100, None)
                cv2.circle(img, (lineInfo[4], lineInfo[5]),
                           15, (0, 255, 0), cv2.FILLED)

    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED),
    cv2.putText(img, f'{int(volPer)}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)
    
    cVol=int(volume.GetMasterVolumeLevelScalar()*100)
    
    cv2.putText(img, f'VOL SET: {int(cVol)}', (400, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)


    cTime = time.time()
    fps = 1 / (cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    cv2.imshow("img", img)
    cv2.waitKey(1)
