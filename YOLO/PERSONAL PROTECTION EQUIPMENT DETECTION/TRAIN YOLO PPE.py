from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.train(data = "E:\Downloads\Construction Site Safety.v30-raw-images_latestversion.yolov8\data.yaml", epochs = 50, imgsz = 640)

metrics = model.val()

