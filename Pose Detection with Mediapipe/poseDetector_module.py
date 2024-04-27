import mediapipe as mp
import time
import math
import cv2

class poseDetector():
    def __init__(self, mode = False, smooth_landmarks=True, enable_segmentation=False,
               smooth_segmentation=True, detection_confidence=0.5, track_confidence=0.5):
        self.mode = mode
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.smooth_landmarks = smooth_landmarks
        self.detection_confidence = detection_confidence
        self.track_confidence = track_confidence
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, 1, self.smooth_landmarks, self.enable_segmentation,
                   self.smooth_segmentation, self.detection_confidence, self.track_confidence)
        
    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img
    
    def findPosition(self, img, draw=True):
        self.landmark_list = []
        if self.results.pose_landmarks:
            for ID, landmark in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(ID, landmark)
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                self.landmark_list.append([ID, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.landmark_list
    
    def findAngle(self, img, p1, p2, p3, draw=True):
        # Get the landmarks
        x1, y1 = self.landmark_list[p1][1:]
        x2, y2 = self.landmark_list[p2][1:]
        x3, y3 = self.landmark_list[p3][1:]
        # Calculate the Angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360
        # print(angle)
        # Draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return angle
    
def main():
    cap = cv2.VideoCapture("E:\\Downloads\\Hurdles (super slow motion).mp4")
    previous_time = 0
    detector = poseDetector()
    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        landmark_list = detector.findPosition(img, draw=False)
        if len(landmark_list) != 0:
            print(landmark_list[17])
            cv2.circle(img, (landmark_list[17][1], landmark_list[17][2]), 15, (0, 0, 255), cv2.FILLED)
        current_time = time.time()
        fps = 1 / (current_time - previous_time)
        previous_time = current_time
        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        
if __name__ == "__main__":
    main()