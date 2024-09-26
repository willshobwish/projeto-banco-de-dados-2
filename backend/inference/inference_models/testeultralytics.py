from ultralytics import YOLO
from PIL import Image
import os

# Load the YOLO model
model = YOLO(r"E:\Sistema\Downloads\yolov8x.pt")

# Function for segmenting and saving detected objects
def segmentation(image_path: str):
    # Inference on the image
    results = model(image_path)

    # Load the original image using PIL
    original_image = Image.open(image_path)

    # Directory to save segments
    output_dir = "output_segments"
    os.makedirs(output_dir, exist_ok=True)

    # Access the first result in the list (assuming only one image is processed)
    result = results[0]

    # Iterate over detected objects and save segments
    for i, box in enumerate(result.boxes.xyxy):  # Access the bounding boxes
        xmin, ymin, xmax, ymax = map(int, box)  # Convert coordinates to integer

        # Crop the segment from the original image
        segment = original_image.crop((xmin, ymin, xmax, ymax))

        # Save the segment
        segment_path = os.path.join(output_dir, f"segment_{i+1}.jpg")
        segment.save(segment_path)

        print(f"Saved segment {i+1} at {segment_path}")

# Call the segmentation function
segmentation(r'assets\pexels-joshsorenson-139303.jpg')
