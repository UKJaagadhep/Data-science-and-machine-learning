import cv2
import time
import handDetector_module as hdm
import os

cam_width, cam_height = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, cam_width)
cap.set(4, cam_height)

#STORE ALL FINGER IMAGES 0 TO 5 IN overlayList LIST.
overlayList = []
folderPath = "FingerImages"
myList = os.listdir(folderPath)
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    #print(f'{folderPath}/{imPath}')
    image = cv2.resize(image, (130, 130))
    overlayList.append(image)
#print(len(overlayList))

detector = hdm.handDetector()

fingerTipIds = [4, 8, 12, 16, 20] #FINGER TIP LANDMARK IDS

previous_time = 0

while True:
    success, img = cap.read()
    
    img = detector.findHands(img)
    landmark_list = detector.findPosition(img, draw=False)
    # print(landmark_list)
    
    if len(landmark_list) != 0:
        fingers = []
        
        #CHECKING IF FINGERS ARE OPEN OR CLOSED
        #FOR THUMB
        #OPEN IF TIP IS MORE IN RIGHT DIRECTION THAN LANDMARK BELOW IT FOR LEFT HAND
        if landmark_list[fingerTipIds[0]][1] < landmark_list[fingerTipIds[0] - 1][1]: #WE USE THE CONDITION IN REVERSE BECAUSE THE CAMERA CHANGES LEFT AND WRITE
            fingers.append(1)
        else:
            fingers.append(0)
            
        #FOR OTHER 4 FINGERS
        #OPEN IF TIP IS HIGHER THAN LANDMARK BELOW IT
        for ID in range(1, 5):
            if landmark_list[fingerTipIds[ID]][2] < landmark_list[fingerTipIds[ID] - 2][2]: #FINGER OPEN
                #print(ID, "open")
                fingers.append(1)
            else: #FINGER CLOSED
                fingers.append(0)
        # print(fingers)
        
        #COUNTING OPEN FINGERS
        totalFingers = fingers.count(1)
        print(totalFingers)
        
        #OVERLAYING FINGER IMAGES ON BOTTOM RIGHT CORNER 
        img[350:480, 510:640] = overlayList[totalFingers]
        
        cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 25)
        
    current_time = time.time()
    fps = 1/(current_time - previous_time)
    previous_time = current_time
    cv2.putText(img, f'FPS : {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 0), 2)
    
    cv2.imshow("Image", img)
    cv2.waitKey(1)