from ultralytics import YOLO
from pathlib import Path
from fastapi import UploadFile
import shutil

# Load a COCO-pretrained YOLO11n model
model = YOLO("yolo11n.pt")

# Train the model on the COCO8 example dataset for 100 epochs
results = model.train(data="coco8.yaml", epochs=100, imgsz=640)

# Run inference with the YOLO11n model on the 'bus.jpg' image
results = model("path/to/bus.jpg")

def save_image(file: UploadFile, upload_dir: Path):
    image_path = upload_dir / file.filename
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return image_path
