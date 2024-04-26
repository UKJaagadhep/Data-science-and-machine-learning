import cv2
import cvzone
from ultralytics import YOLO
import math

'''#For Webcam
cap = cv2.VideoCapture(0)  
cap.set(3, 1280)
cap.set(4, 720)'''

cap = cv2.VideoCapture("E:\\Downloads\\ppe-2-1.mp4") #FOR VIDEOS

model = YOLO("D:\\OneDrive\\Desktop\\runs\\detect\\train\\weights\\best.pt")

classNames = ['Excavator', 'Gloves', 'Hardhat', 'Ladder', 'Mask', 'NO-Hardhat', 'NO-Mask', 'NO-Safety Vest',
              'Person', 'SUV', 'Safety Cone', 'Safety Vest', 'bus', 'dump truck', 'fire hydrant', 'machinery',
              'mini-van', 'sedan', 'semi', 'trailer', 'truck and trailer', 'truck', 'van', 'vehicle', 'wheel loader']

myColor = (0, 0, 255) #INITIALIZING BOUNDING BOX COLOR

while True:
    success, img = cap.read()
    results = model(img, stream = True)
    
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]                                    
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            confidence_score = math.ceil((box.conf[0]*100)) / 100 #HAS 2 DECIMAL POINTS
            
            class_name_index = int(box.cls[0])
            currentClass = classNames[class_name_index]
 
            if confidence_score>0.5:
                #WHEN CLASSES ARE DETECTED, WE DISPLAY THE RECTANGLE IN DIFFERENT COLOR
                if currentClass =='NO-Hardhat' or currentClass =='NO-Safety Vest' or currentClass == "NO-Mask":
                    myColor = (0, 0,255) #RED
                elif currentClass =='Hardhat' or currentClass =='Safety Vest' or currentClass == "Mask":
                    myColor =(0,255,0) #GREEN
                else:
                    myColor = (255, 0, 0) #BLUE
 
                cvzone.putTextRect(img, f'{currentClass} {confidence_score}',
                                   (max(0, x1), max(35, y1)), scale=1, thickness=1,colorB=myColor,
                                   colorT=(255,255,255),colorR=myColor, offset=5)
                cv2.rectangle(img, (x1, y1), (x2, y2), myColor, 3)
    
    cv2.imshow("Image : ",img)
    cv2.waitKey(1)
    

