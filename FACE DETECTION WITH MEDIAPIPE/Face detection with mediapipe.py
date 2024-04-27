import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture("D:\\OneDrive\\Desktop\\FACE DETECTION WITH MEDIAPIPE\\Jenna Ortega death stare vs sigma death stares..mp4")

mpFaceDetection = mp.solutions.face_detection
faceDetection = mpFaceDetection.FaceDetection()
mpDraw = mp.solutions.drawing_utils


previous_time = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceDetection.process(imgRGB)
    
    if results.detections:
        for ID, detection in enumerate(results.detections):
            # print(ID, detection)
            # print(detection.score)
            # print(detection.location_data.relative_bounding_box) #GIVES XMIN, YMIN, WIDTH, HEIGHT
            h, w, c = img.shape
            bounding_box_c = detection.location_data.relative_bounding_box
            bounding_box = int(bounding_box_c.xmin * w), int(bounding_box_c.ymin * h), int(bounding_box_c.width * w), int(bounding_box_c.height * h)
            '''cv2.rectangle(img, bounding_box, (255, 0, 255), 2)
            cv2.putText(img, f'{int(detection.score[0] * 100)}%', (bounding_box[0], bounding_box[1] - 20), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
            '''
            mpDraw.draw_detection(img, detection)
            
    current_time = time.time()
    fps = 1/(current_time - previous_time)
    previous_time = current_time
    
    cv2.putText(img, f'FPS : {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2) 
        
    cv2.imshow("Image:", img)
    cv2.waitKey(1)

