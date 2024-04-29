import cv2
import time
import numpy as np
import poseDetector_module as pdm

'''cam_width, cam_height = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, cam_width)
cap.set(4, cam_height)'''
cap = cv2.VideoCapture("D:\\OneDrive\\Desktop\\Dumbbell bicep curls.mp4")

detector = pdm.poseDetector()

count = 0
direction = 0
# DIRECTION = 0 WHEN ARM GOES UP AND DIRECTION = 1 WHEN ARM COMES DOWN. ACTS LIKE A FLAG AND PREVENTS DUPLICATE VALUES FROM BEING COUNTED
#SO A FULL CURL MUST HAVE BOTH OF THESE 0 AND 1

previous_time = 0

while True:
    success, img = cap.read()
    
    img = detector.findPose(img, False)
    landmark_list = detector.findPosition(img, False)
    
    if len(landmark_list) != 0:
        #TAKE THE LANDMARKS OF THE MOVING PARTS LIKE ARM IN BICEP CURL
        
        #LEFT ARM LANDMARKS
        angle = detector.findAngle(img, 11, 13, 15)
        '''ANGLE RANGE : [215, 350]'''
        
        #RIGHT ARM LANDMARKS
        #angle = detector.findAngle(img, 12, 14, 16)
        
        if angle < 150: #FIXING ANOMALIES
            angle = 350
        
        percentage = np.interp(angle, [215, 350], [0, 100]) #CONVERTING FROM ANGLE RANGE TO PERCENTAGE RANGE
        #print(percentage)
        
        color = (255, 0, 255)
        
        #CHECKING FOR BICEP CURLS
        if percentage == 100:
            if direction == 0:
                count += 0.5
                direction = 1
                color = (0, 255, 0)
                
        if percentage == 0:
            if direction == 1:
                count += 0.5
                direction = 0
                color = (0, 255, 0)
                
        #print(count)
                
        #DISPLAYING COUNT
        #cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (25, 670), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 20)
        #print(img.shape)
        
        #DISPLAYING BAR WITH PERCENTAGE OF BICEP UP
        bar = np.interp(angle, [211, 350], [680, 500]) #CONVERTING FROM ANGLE RANGE TO BAR'S Y COORDINATE RANGE
        cv2.rectangle(img, (320, 500), (380, 680), color, 3)
        cv2.rectangle(img, (320, int(bar)), (380, 680), color, cv2.FILLED)
        cv2.putText(img, f'{int(percentage)} %', (300, 480), cv2.FONT_HERSHEY_PLAIN, 2, (255, 50, 255), 4)
    
    current_time = time.time()
    fps = 1/(current_time - previous_time)
    previous_time = current_time
    cv2.putText(img, f'FPS : {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 0), 2)
    
    cv2.imshow("Image", img)
    cv2.waitKey(1)

