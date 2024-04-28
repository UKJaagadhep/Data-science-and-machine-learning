import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture("D:\\OneDrive\\Desktop\\FACE DETECTION WITH MEDIAPIPE\\Jenna Ortega death stare vs sigma death stares..mp4")

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces = 2)
drawSpec = mpDraw.DrawingSpec(thickness = 1, circle_radius = 2) #DRAWING SPECIFICATIONS FOR CONNECTIONS 

previous_time = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)
    if results.multi_face_landmarks:
        for each_face in results.multi_face_landmarks:
            mpDraw.draw_landmarks(img, each_face, mpFaceMesh.FACEMESH_TESSELATION, landmark_drawing_spec = drawSpec, connection_drawing_spec = drawSpec)
            for ID, landmark in enumerate(each_face.landmark):
                print(ID, landmark)
                h, w, c = img.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                print(ID,  cx, cy)
    
    current_time = time.time()
    fps = 1/(current_time - previous_time)
    previous_time = current_time
    
    cv2.putText(img, f'FPS : {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2) 
        
    cv2.imshow("Image:", img)
    cv2.waitKey(1)