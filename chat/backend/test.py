from transformers import pipeline

# Load a pre-trained text generation model
generator = pipeline("text-generation", model="meta-llama/Llama-3.1-8B-Instruct")

# Simple chatbot loop
def chatbot():
    print("Chatbot: Hello! How can I help you?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye!")
            break
        
        # Generate a response based on the user input
        response = generator(user_input, max_length=50, num_return_sequences=1)
        
        # Extract the generated text
        bot_response = response[0]['generated_text']
        print(f"Chatbot: {bot_response}")

if __name__ == "__main__":
    chatbot()
