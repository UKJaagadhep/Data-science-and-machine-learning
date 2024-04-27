import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture("E:\\Downloads\\Hurdles (super slow motion).mp4")

mpPose = mp.solutions.pose
pose = mpPose.Pose()

mpDraw = mp.solutions.drawing_utils

previous_time = 0
current_time = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    #print(results.pose_landmarks)
    
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for ID, landmark in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            cx, cy = int(landmark.x * w), int(landmark.y * h)
            #if ID == 15:
            cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
                
    current_time = time.time()
    fps = 1/(current_time - previous_time)
    previous_time = current_time
    
    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3) 
        
    cv2.imshow("Image:", img)
    cv2.waitKey(1)
