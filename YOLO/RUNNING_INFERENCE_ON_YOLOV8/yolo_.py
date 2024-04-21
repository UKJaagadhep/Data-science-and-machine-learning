from ultralytics import YOLO

# LOAD MODEL
model = YOLO("yolov8n.pt")

# INFERENCE
results = model("C:\\Users\\ukjag\\fiftyone\\open-images-v7\\images\\train\\e29c237b476f0a1c.jpg")

# FIRST ELEMENT OF RESULTS IS THE INFERENCE RESULTS FOR FIRST IMAGE INPUT
print(results)
result = results[0]

# SHOW ANNOTATED IMAGE
result.show()
