import cv2
import mediapipe as mp
import time

class FaceMeshDetector():
    def __init__(self, staticMode = False, maxFaces = 2, minDetectionConfidence = 0.5, minTrackConfidence = 0.5):
        self.staticMode = staticMode
        self.maxFaces = maxFaces
        self.minDetectionConfidence = minDetectionConfidence
        self.minTrackConfidence = minTrackConfidence

        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(self.staticMode, self.maxFaces, False, self.minDetectionConfidence, self.minTrackConfidence)
        self.drawSpec = self.mpDraw.DrawingSpec(thickness = 1, circle_radius = 2)

    def findFaceMesh(self, img, draw = True):
        self.imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceMesh.process(self.imgRGB)
        faces = []
        if self.results.multi_face_landmarks:
            for each_face in self.results.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, each_face, self.mpFaceMesh.FACEMESH_TESSELATION, self.drawSpec, self.drawSpec)
                face = []
                for ID,landmark in enumerate(each_face.landmark):
                    #print(landmark)
                    h, w, c = img.shape
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    #cv2.putText(img, str(ID), (cx, cy), cv2.FONT_HERSHEY_PLAIN, 0.7, (0, 255, 0), 1)
                    #print(ID, cx, cy)
                    face.append([cx, cy])
                faces.append(face)
        return img, faces

def main():
    cap = cv2.VideoCapture("D:\\OneDrive\\Desktop\\FACE DETECTION WITH MEDIAPIPE\\Jenna Ortega death stare vs sigma death stares..mp4")
    previous_time = 0
    detector = FaceMeshDetector(maxFaces=2)
    while True:
        success, img = cap.read()
        img, faces = detector.findFaceMesh(img)
        if len(faces)!= 0:
            print(faces[0])
        current_time = time.time()
        fps = 1 / (current_time - previous_time)
        previous_time = current_time
        cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()