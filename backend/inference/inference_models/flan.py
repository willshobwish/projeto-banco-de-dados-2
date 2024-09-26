
from transformers import T5Tokenizer, T5ForConditionalGeneration

tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-large")
model = T5ForConditionalGeneration.from_pretrained(
    "google/flan-t5-large", device_map="auto")

input_text = 'Your task is to generate a text with the visual details of an image description: "The image shows a busy street with many people walking. Focus on the key elements: What color are the people wearing? Red. Is there a car visible? Yes. Is there a bicycle present? No."'

input_ids = tokenizer(input_text, return_tensors="pt").input_ids

outputs = model.generate(input_ids, max_length=1000)
print(tokenizer.decode(outputs[0]))
