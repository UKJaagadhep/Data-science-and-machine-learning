import cv2
import time
import math
import numpy as np
import handDetector_module as hdm
#FOR AUDIO
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cam_width, cam_height = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, cam_width)
cap.set(4, cam_height)

detector = hdm.handDetector()

#INITIALIZING AUDIO DEVICES AND ACCESS
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()

#WE GET THE VOLUME RANGE OF OUR DEVICE
volRange = volume.GetVolumeRange()
#print(volRange)
minVol = volRange[0] # -96.0
maxVol = volRange[1] # 0.0

volBar = 400
volPer = 0
vol = 0

previous_time = 0

while True:
    success, img = cap.read()
    
    img = detector.findHands(img)
    landmark_list = detector.findPosition(img, draw = False)
    
    if len(landmark_list) != 0:
        #LANDMARK 4 IS THUMB TIP AND LANDMARK 8 IS INDEX FINGER TIP
        #print(landmark_list[4], landmark_list[8])
        x1, y1 = landmark_list[4][1], landmark_list[4][2]
        x2, y2 = landmark_list[8][1], landmark_list[8][2]
        
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        
        #DRAWING A LINE BETWEEN THUMB TIP AND INDEX FINGER TIP
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2 #CENTER OF THE LINE
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED) #DRAWING A CIRCLE ON CENTER OF THE LINE
        
        #WE CHANGE THE VOLUME BASED ON THE DISTANCE OF THE LINE I.E., THE DISTANCE BETWEEN THE THUMB TIP AND INDEX FINGER TIP
        length = math.hypot(x2 - x1, y2 - y1) #DISTANCE OF LINE I.E., THE DISTANCE BETWEEN THE THUMB TIP AND INDEX FINGER TIP
        #print(length)
        '''RANGE OF LENGTH VALUES MEASURED USING MOVING HAND AND PRINT
        [30, 300]
        WE NEED TO CONVERT THIS RANGE TO OUR VOLUME RANGE [-96.0, 0.0] '''
        
        vol = np.interp(length, [30, 300], [minVol, maxVol]) #CONVERTING LENGTH RANGE TO VOLUME RANGE
        print(int(length), vol)
        
        #SET VOLUME ACCORDING TO LENGTH
        volume.SetMasterVolumeLevel(vol, None)
        
        if length < 30: #ACTS LIKE A BUTTON TO INDICATE LOWER LIMIT
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
            
        #DISPLAYING VOLUME BAR
        cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
        volBar = np.interp(length, [30, 300], [400, 150]) #CONVERTING LENGTH RANGE TO RECTANGLE Y RANGE [150, 400]
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
        
        #DISPLAYING VOLUME TEXT
        volPer = np.interp(length, [30, 300], [0, 100]) #CONVERTING LENGTH RANGE TO [0, 100] INDICATING VOLUME PERCENTAGE
        cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
        
    current_time = time.time()
    fps = 1/(current_time - previous_time)
    previous_time = current_time
    cv2.putText(img, f'FPS : {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 0), 2)
    
    cv2.imshow("Image", img)
    cv2.waitKey(1)