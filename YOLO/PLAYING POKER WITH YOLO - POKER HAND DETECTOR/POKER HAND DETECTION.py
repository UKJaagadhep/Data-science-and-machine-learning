from ultralytics import YOLO
import cv2
import cvzone
import math
import PokerHandFunction
 
cap = cv2.VideoCapture(0)  # For Webcam
cap.set(3, 1280)
cap.set(4, 720)
 
model = YOLO("D:\\OneDrive\\Desktop\\PLAYING POKER WITH YOLO - POKER HAND DETECTOR\\playingCards.pt")
classNames = ['10C', '10D', '10H', '10S',
              '2C', '2D', '2H', '2S',
              '3C', '3D', '3H', '3S',
              '4C', '4D', '4H', '4S',
              '5C', '5D', '5H', '5S',
              '6C', '6D', '6H', '6S',
              '7C', '7D', '7H', '7S',
              '8C', '8D', '8H', '8S',
              '9C', '9D', '9H', '9S',
              'AC', 'AD', 'AH', 'AS',
              'JC', 'JD', 'JH', 'JS',
              'KC', 'KD', 'KH', 'KS',
              'QC', 'QD', 'QH', 'QS']

while True:
    success, img = cap.read()
    results = model(img, stream = True)
    hand = [] #HAND SHOULD BE CLEARED AFTER EACH ITERATION OR VIDEO
    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            w, h = x2 - x1, y2 - y1
             
            cvzone.cornerRect(img, (x1, y1, w, h))
             
            confidence_score = math.ceil((box.conf[0]*100)) / 100 #HAS 2 DECIMAL POINTS
            
            class_name_index = int(box.cls[0])
            current_class = classNames[class_name_index]
             
            cvzone.putTextRect(img, f'{current_class} {confidence_score}', (max(0, x1), max(35, y1)), scale=1, thickness=1)
             
            if conf > 0.5:
                hand.append(current_class)
     
    hand = list(set(hand)) #SINCE EACH CARD HAS RANK IN 2 PLACES, WE WANT TO DETECT IT ONLY ONCE IF BOTH TOP AND BOTTOM ARE DETECTED        
     
    if len(hand) == 5:
        results = PokerHandFunction.findPokerHand(hand)
        cvzone.putTextRect(img, f'Your Hand: {results}', (300, 75), scale=3, thickness=5)   
    cv2.imshow("Image", img)
    cv2.waitKey(1)    