import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-chatbot',
  templateUrl: './chatbot.page.html',
  styleUrls: ['./chatbot.page.scss'],
})
export class ChatbotPage {
  messages: { text: string, user: string }[] = [];
  newMessage: string = '';
  userId: string = 'user1'; // Placeholder, you can generate a unique ID per session

  constructor(private http: HttpClient) {}

  sendMessage() {
    if (this.newMessage.trim().length === 0) return;

    // Add user's message to the chat window
    this.messages.push({ text: this.newMessage, user: 'me' });

    // Prepare the request body
    const requestBody = {
      user_id: this.userId,
      message: this.newMessage,
    };

    // Send the message to the backend
    this.http.post<{ response: string }>('http://localhost:8000/chat/', requestBody)
      .subscribe((res) => {
        // Add bot's response to the chat window
        this.messages.push({ text: res.response, user: 'bot' });
      });

    // Clear the input field
    this.newMessage = '';
  }
}
