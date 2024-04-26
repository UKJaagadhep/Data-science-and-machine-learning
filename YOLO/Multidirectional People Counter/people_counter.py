import cv2
import cvzone
from ultralytics import YOLO
import math
from sort import *
import numpy

cap = cv2.VideoCapture("E:\\Downloads\\people.mp4") 

model = YOLO("yolov8n.pt")

mask = cv2.imread("E:\\Downloads\\MASK PEOPLE.png")
mask = cv2.resize(mask, (1280, 720)) #img SHAPE = mask SHAPE
#print(mask.shape)

img_graphics = cv2.imread("E:\\Downloads\\graphics-PEOPLE.png", cv2.IMREAD_UNCHANGED)

#TRACKER
tracker = Sort(max_age = 20, min_hits = 3, iou_threshold = 0.3)

limits_up = [103, 161, 296, 161]
limits_down = [527, 489, 735, 489] #LIMITS OF THE LINE [X1, Y1, X2, Y2]

total_count_up = []
total_count_down = []

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

while True:
    success, img = cap.read()
    #print("img ", img.shape)
    imgRegion = cv2.bitwise_and(img, mask)
    
    img = cvzone.overlayPNG(img, img_graphics, (730, 260))
    
    results = model(imgRegion, stream = True)
    
    #INITIALIZING DETECTIONS
    detections = np.empty((0, 5))
    
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0] #THIS FORMAT IS EASIER TO WORK WITH IN OPENCV FOR BOUNDING BOXES1)                     
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            ''' #FOR DOING WITH OPENCV INSTEAD OF CVZONE : 
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3) #(0, 255, 0) REPRESENTS COLOR   #3 REPRESENTS THICKNESS'''
                        
            w, h = x2-x1, y2-y1
            
            bbox = x1, y1, w, h
            
            #cvzone.cornerRect(img, bbox, rt = 3) #rt IS RECTANGLE THICKNESS
                             
            confidence_score = math.ceil((box.conf[0]*100)) / 100 #HAS 2 DECIMAL POINTS
            
            class_name_index = int(box.cls[0])
            
            current_class = classNames[class_name_index]
            
            if current_class == "PERSON" and confidence_score > 0.3:
                #TO ADD DETECTED CAR TO DETECTIONS ARRAY
                detected = np.array([x1, y1, x2, y2, confidence_score])
                detections = np.vstack((detections, detected))
        
    resultsTracker = tracker.update(detections)
    
    cv2.line(img, (limits_up[0], limits_up[1]), (limits_up[2], limits_up[3]), (0, 0, 255), 5)
    cv2.line(img, (limits_down[0], limits_down[1]), (limits_down[2], limits_down[3]), (0, 0, 255), 5)
    
    for result in resultsTracker:
        x1, y1, x2, y2, id_ = result
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        w, h = x2-x1, y2-y1
        bbox = x1, y1, w, h
        
        cvzone.cornerRect(img, bbox, rt = 2, colorR = (255, 0, 0))
        cvzone.putTextRect(img, f' {int(id_)}', (max(0, x1), max(35, y1)), scale = 2, thickness = 3, offset = 4)
        #offset IS CORNER THICKNESS
        
        # CIRCLE FOR OBJECT CENTER
        x_center, y_center = x1 + (w//2), y1 + (h//2)
        cv2.circle(img, (x_center, y_center), 5, (125, 0, 255), cv2.FILLED) # 5 IS RADIUS   #cv2.FILLED IS THICKNESS. IT TELLS TO FILL THE CIRCLE COMPLETELY
        
        if limits_up[0] < x_center < limits_up[2] and limits_up[1] - 20 < y_center < limits_up[3] + 20:
            if total_count_up.count(id_) == 0: 
                total_count_up.append(id_)
                #WE SHOW SAME LINE IN DIFFERENT COLOR WHEN COUNTED OBJECT
                cv2.line(img, (limits_up[0], limits_up[1]), (limits_up[2], limits_up[3]), (0, 255, 0), 5)
                
        if limits_down[0] < x_center < limits_down[2] and limits_down[1] - 20 < y_center < limits_down[3] + 20:
            if total_count_down.count(id_) == 0: 
                total_count_down.append(id_)
                cv2.line(img, (limits_down[0], limits_down[1]), (limits_down[2], limits_down[3]), (0, 255, 0), 5)
                
    #TO DISPLAY TOTAL COUNT IN THE TOP LEFT CORNER 
    cv2.putText(img, str(len(total_count_up)), (930, 340), cv2.FONT_HERSHEY_PLAIN, 5, (140, 200, 80), 7)
    cv2.putText(img, str(len(total_count_down)), (1190, 340), cv2.FONT_HERSHEY_PLAIN, 5, (50, 50, 230), 7)
    
    cv2.imshow("Image : ",img)
    #cv2.imshow("Image Region : ", imgRegion)
    cv2.waitKey(1)


