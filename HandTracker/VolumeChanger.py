import cv2
import mediapipe as mp
import numpy as np
import time
import HandTracker as ht
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

volume_range = volume.GetVolumeRange()
# volume.SetMasterVolumeLevel(-63, None)
# print(volume_range)

def getAngle(a, b, c):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang if ang > 0 else 360 + ang 


# exit(1)
ptime = 0
ctime = 0
cap = cv2.VideoCapture(0)
detector = ht.handDetector()
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        x3, y3 = lmList[2][1], lmList[2][2]
        
        cv2.circle(img, (x3,y3), 15, (255,0,255), cv2.FILLED)

        distance = np.sqrt((x1-x2)**2 + (y1-y2)**2)
        
        angle = getAngle((x1,y1),(x3,y3),(x2,y2))
        angle = min(angle, 360 - angle)

        min_angle = 15
        max_angle = 80

        angle = max(min_angle, angle)
        angle = min(max_angle, angle)
        absolute_angle = (angle - min_angle) / (max_angle - min_angle)

        if angle > min_angle:
            cv2.circle(img, (x1,y1), 15, (255,0,255), cv2.FILLED)
            cv2.circle(img, (x2,y2), 15, (255,0,255), cv2.FILLED)
            
            volume_value = -63 + int(absolute_angle * (63))
        
        else:
            cv2.circle(img, (x1,y1), 15, (0,255,0), cv2.FILLED)
            cv2.circle(img, (x2,y2), 15, (0,255,0), cv2.FILLED)
            
            volume_value = -63.5 

        volume.SetMasterVolumeLevel(volume_value, None)

    ctime = time.time()
    fps = 1/(ctime - ptime)
    ptime = ctime
    cv2.putText(img, f'FPS: {int(fps)}', (40,50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)