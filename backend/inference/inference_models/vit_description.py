from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch
import os
from PIL import Image

model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

max_length = 100
num_beams = 10
gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

def predict_step(image_folder:str,text_path:str):
  images = []
  for image_path in os.listdir(image_folder):
    image_path = os.path.join(image_folder,image_path)
    i_image = Image.open(image_path)
    if i_image.mode != "RGB":
      i_image = i_image.convert(mode="RGB")

    images.append(i_image)

  pixel_values = feature_extractor(images=images, return_tensors="pt").pixel_values
  pixel_values = pixel_values.to(device)

  output_ids = model.generate(pixel_values, **gen_kwargs)

  preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
  preds = [pred.strip() for pred in preds]
  with open(text_path, "w") as file:
    # Iterate over the array and write each item on a new line
    for image_name, prediction in zip(os.listdir(image_folder),preds):
        file.write(f"{image_name}: {prediction}\n")



# [print(i) for i in predict_step([os.path.join(r'output_segments',x) for x in os.listdir(r'output_segments')])]
predict_step(r'output_segments','test.txt')