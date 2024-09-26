import os
from PIL import Image
from transformers import (
    Blip2Processor,
    Blip2ForConditionalGeneration,
    BlipProcessor,
    BlipForConditionalGeneration,BlipForQuestionAnswering
)
import torch

# Load the model and processor
# processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
# model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b", device_map="auto")

processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
# Define the folder with images
image_folder = r"output_segments"
output_file = "image_questions.txt"
questions = ["What color is using?","There is a car?", "There is a bicycle?", "Give me an insight of image"]
# Create or open the text file for writing
with open(output_file, "w") as f:
    # Iterate over all files in the folder
    for image_name in os.listdir(image_folder):
        if image_name.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
            image_path = os.path.join(image_folder, image_name)
            print(f"Processing {image_name}...")

            # Load the image
            raw_image = Image.open(image_path).convert("RGB")

            # Generate the description
            for question in questions:
                inputs = processor(
                    raw_image,
                    question,
                    return_tensors="pt",)
                out = model.generate(**inputs)
                description = processor.decode(
                    out[0], skip_special_tokens=True).strip()

                # Write the filename and description to the text file
                f.write(f"{image_name}:{question} {description}\n")
                print(f"Description for {image_name}: {description}")

print(f"Descriptions saved to {output_file}")
