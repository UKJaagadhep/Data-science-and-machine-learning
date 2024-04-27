import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands #IMPORT HAND TRACKING MODEL
hands = mpHands.Hands() #INITIALIZES A HAND TRACKING MODEL
mpDraw = mp.solutions.drawing_utils #DRAWS ANNOTATIONS AND VISUALIZATIONS ON TOP OF THE OUTPUTS OR IMAGES

previous_time = 0
current_time = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    results = hands.process(imgRGB) #PROCESSES OR RUN INFERENCE ON IMAGE
    #print(results.multi_hand_landmarks) #21 LANDMARKS FOR EACH HAND AND X,Y,Z FOR EACH LANDMARK
    
    if results.multi_hand_landmarks:
        for each_hand in results.multi_hand_landmarks:
            for ID, landmark in enumerate(each_hand.landmark):
                #print(ID, landmark)
                h, w, c = img.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h) #cx AND cy ARE THE ACTUAL (NOT NORMALIZED) X AND Y COORDINATES
                #print(ID, cx, cy)
                # if ID == 4:
                cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                #WE CAN STORE CX, XY OF REQUIRED LANDMARKS IN A LIST AND USE IT LATER AS PER OUR TASK
            mpDraw.draw_landmarks(img, each_hand, mpHands.HAND_CONNECTIONS)
            #WE DISPLAY ON IMG AND NOT IMGRGB BECAUSE IMAGE IS DISPLAYED IN BGR FORMAT
            #mpHands.HAND_CONNECTIONS IS TO DRAW CONNECTING LINES BETWEEN THE LANDMARKS. THIS HELPS US TO VISUALIZE OUR HAND POSITION EASILY. 
    
    current_time = time.time()
    fps = 1/(current_time - previous_time)
    previous_time = current_time
    
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    
    cv2.imshow("Image:", img)
    cv2.waitKey(1)