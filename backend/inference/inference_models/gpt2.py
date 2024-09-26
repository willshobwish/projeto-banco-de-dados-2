from transformers import pipeline, set_seed
generator = pipeline('text-generation', model='gpt2')
set_seed(42)
generator("the image have a lot of people walking around the street", max_length=50, num_return_sequences=5)