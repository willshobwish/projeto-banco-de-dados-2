from fastapi import FastAPI, HTTPException
from transformers import pipeline, Conversation
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# Load Hugging Face conversational model (DialoGPT or BlenderBot)
chatbot = pipeline("conversational", model="microsoft/DialoGPT-medium")

# Store conversations for each user
conversations: Dict[str, Conversation] = {}

# Request model for the chatbot
class ChatRequest(BaseModel):
    user_id: str
    message: str

# Chat endpoint that keeps conversation context for each user
@app.post("/chat/")
async def chat(request: ChatRequest):
    user_id = request.user_id
    user_message = request.message

    if user_id not in conversations:
        # Create a new conversation for this user
        conversations[user_id] = Conversation(user_message)
    else:
        # Append the message to the existing conversation
        conversations[user_id].add_user_input(user_message)

    try:
        # Get the chatbot's response using the conversation context
        result = chatbot(conversations[user_id])
        response = result.generated_responses[-1]  # Get the latest response
        return {"user_id": user_id, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
