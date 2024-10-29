import torch
import cv2
import os
import numpy as np

# Check if CUDA is available and set device accordingly
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Load the YOLOv5 model on the appropriate device (CPU or GPU)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True).to(device)

# Set the image directory and output directory
image_dir = r'D:\Sistema\Desktop\Nova pasta'  # Replace with your image directory
output_dir = r'D:\Sistema\Desktop\Saida'  # Replace with your output directory
os.makedirs(output_dir, exist_ok=True)

# Process each image in the directory
for image_file in os.listdir(image_dir):
    if image_file.endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(image_dir, image_file)

        # Read the image
        img = cv2.imread(image_path)

        # Convert image to RGB as YOLO expects RGB images
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Move the image to the device (GPU/CPU)
        # img_tensor = torch.from_numpy(img_rgb).to(device)
        # img_tensor = img_tensor.permute(2, 0, 1).float() / 255.0  # Change to C x H x W format and normalize
        # img_tensor = img_tensor.unsqueeze(0)  # Add batch dimension

        # Perform inference
        results = model(img_rgb)

        # Get bounding boxes and labels
        boxes = results.xyxy[0]  # This will still be on the GPU

        # Convert boxes to NumPy array by moving them to CPU
        # boxes = boxes.cpu().numpy()

        # Extract and save segments
        for i, box in enumerate(boxes):
            x1, y1, x2, y2, conf, cls = box.astype(int)
            segment = img[y1:y2, x1:x2]  # Crop the segment

            # Save the segment with a unique name
            segment_filename = f"{os.path.splitext(image_file)[0]}_segment_{i}.png"
            segment_path = os.path.join(output_dir, segment_filename)
            cv2.imwrite(segment_path, segment)

        print(f"Processed {image_file}, saved segments to {output_dir}")
