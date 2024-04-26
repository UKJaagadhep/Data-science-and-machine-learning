from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.train(data = "E:\Downloads\Playing Cards.v3-original_raw-images.yolov8\data.yaml", epochs = 10, imgsz = 640)

metrics = model.val()

#yolo

