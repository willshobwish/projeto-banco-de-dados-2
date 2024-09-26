import os
from PIL import Image
from transformers import Blip2Processor, Blip2ForConditionalGeneration, BlipProcessor, BlipForConditionalGeneration

# Load the model and processor
processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-large")

# Define the folder with images
image_folder = 'output_segments'
output_file = 'image_descriptions.txt'

# Create or open the text file for writing
with open(output_file, 'w') as f:
    # Iterate over all files in the folder
    for image_name in os.listdir(image_folder):
        if image_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            image_path = os.path.join(image_folder, image_name)
            print(f"Processing {image_name}...")

            # Load the image
            raw_image = Image.open(image_path).convert('RGB')

            # Generate the description
            inputs = processor(
                raw_image, text="The image have", return_tensors="pt",)
            out = model.generate(**inputs)
            description = processor.decode(
                out[0], skip_special_tokens=True).strip()

            # Write the filename and description to the text file
            f.write(f"{image_name}: {description}\n")
            print(f"Description for {image_name}: {description}")

print(f"Descriptions saved to {output_file}")
