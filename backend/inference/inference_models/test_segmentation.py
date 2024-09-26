import torch
from PIL import Image
import os

# Load the YOLOv5 model
model = torch.hub.load("ultralytics/yolov5", "yolov5s")


def segmentation(image_path: str):
    # Inference on an image
    # image_path = r"assets\pexels-ekrulila-2332914.jpg"
    results = model(image_path)

    # Load the original image using PIL
    original_image = Image.open(image_path)

    # Directory to save segments
    output_dir = "output_segments"
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over detected objects and save segments
    for i, (xmin, ymin, xmax, ymax) in enumerate(results.xyxy[0][:, :4]):
        # Convert coordinates to integer
        xmin, ymin, xmax, ymax = map(int, [xmin, ymin, xmax, ymax])

        # Crop the segment from the original image
        segment = original_image.crop((xmin, ymin, xmax, ymax))

        # Save the segment
        segment_path = os.path.join(output_dir, f"segment_{i+1}.jpg")
        segment.save(segment_path)

        print(f"Saved segment {i+1} at {segment_path}")


segmentation(r'assets\pexels-joshsorenson-139303.jpg')
