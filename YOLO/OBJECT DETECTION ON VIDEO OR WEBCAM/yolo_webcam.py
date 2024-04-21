import cv2
import cvzone
from ultralytics import YOLO
import math
import time

cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture("E:\\Downloads\\Accident-Detection-System-main\\head_on_collision_100.mp4") #FOR VIDEOS

cap.set(3, 1280) #Prop ID no. 3 is WIDTH #SO HERE WE SET WIDTH = 1280 
cap.set(4, 720) #Prop ID no. 4 is HEIGHT #SO HERE WE SET HEIGHT = 720

'''ANOTHER COMMONLY USED CONVENTION
cap.set(3, 640) 
cap.set(4, 480)'''

model = YOLO("yolov8n.pt")

classNames = ["PERSON", "BICYCLE", "CAR", "MOTORBIKE", "AEROPLANE", "BUS", "TRAIN", "TRUCK", "BOAT",
              "TRAFFIC LIGHT", "FIRE HYDRANT", "STOP SIGN", "PARKING METER", "BENCH", "BIRD", "CAT",
              "DOG", "HORSE", "SHEEP", "COW", "ELEPHANT", "BEAR", "ZEBRA", "GIRAFFE", "BACKPACK", "UMBRELLA",
              "HANDBAG", "TIE", "SUITCASE", "FRISBEE", "SKIS", "SNOWBOARD", "SPORTS BALL", "KITE", "BASEBALL BAT",
              "BASEBALL GLOVE", "SKATEBOARD", "SURFBOARD", "TENNIS RACKET", "BOTTLE", "WINE GLASS", "CUP",
              "FORK", "KNIFE", "SPOON", "BOWL", "BANANA", "APPLE", "SANDWICH", "ORANGE", "BROCCOLI",
              "CARROT", "HOT DOG", "PIZZA", "DONUT", "CAKE", "CHAIR", "SOFA", "POTTEDPLANT", "BED",
              "DININGTABLE", "TOILET", "TVMONITOR", "LAPTOP", "MOUSE", "REMOTE", "KEYBOARD", "CELL PHONE",
              "MICROWAVE", "OVEN", "TOASTER", "SINK", "REFRIGERATOR", "BOOK", "CLOCK", "VASE", "SCISSORS",
              "TEDDY BEAR", "HAIR DRIER", "TOOTHBRUSH"]

prev_frame_time = 0
new_frame_time = 0

while True:
    new_frame_time = time.time()
    
    success, img = cap.read()
    results = model(img, stream = True)
    
    '''In the context of the YOLO class from the ultralytics library, when stream is set to True,
    it indicates that the model should perform inference on a stream of images. This mode is suitable
    when you are processing a continuous video stream, such as from a webcam or a video file.

    Setting stream=True allows the model to optimize its processing for real-time video streams,
    potentially utilizing optimizations such as prefetching images, batching inference requests,
    or other techniques to improve performance and reduce latency.
    
    When stream=True, the YOLO class from the ultralytics library uses generators to process a
    stream of images efficiently. Generators are functions in Python that allow you to generate a
    sequence of values over time, rather than storing them all in memory at once. This is particularly
    useful for scenarios like processing a continuous video stream, where you don't want to load all
    the frames into memory simultaneously.'''
    
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0] #THIS FORMAT IS EASIER TO WORK WITH IN OPENCV FOR BOUNDING BOXES
            '''In YOLO, the results.box.xyxy property contains the coordinates of the bounding boxes
            predicted by the model. The coordinates are in the format [x1, y1, x2, y2], where (x1, y1)
            is the top-left corner of the bounding box and (x2, y2) is the bottom-right corner.'''
                                   
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            ''' #FOR DOING WITH OPENCV INSTEAD OF CVZONE : 
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3) #(0, 255, 0) REPRESENTS COLOR   #3 REPRESENTS THICKNESS'''
                        
            w, h = x2-x1, y2-y1
            
            bbox = x1, y1, w, h
            
            cvzone.cornerRect(img, bbox, rt = 3) #rt IS RECTANGLE THICKNESS
                             
            confidence = math.ceil((box.conf[0]*100)) / 100 #HAS 2 DECIMAL POINTS
            
            class_name_index = int(box.cls[0])
 
            cvzone.putTextRect(img, f'{classNames[class_name_index]} {confidence}', (max(0, x1), max(35, y1)), scale=1, thickness=1)
            #max(35, y1) HAS 35 INSTEAD OF 0 BECAUSE WE WANT TO GIVE SPACE TO TEXT WHICH WILL BE ABOVE THE RECTANGLE
            
    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    print("fps : ",fps)
    
    cv2.imshow("Image : ",img)
    cv2.waitKey(1)
    
