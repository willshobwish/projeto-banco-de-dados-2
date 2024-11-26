import { Injectable } from '@angular/core';
import axios from 'axios';

const API_URL = 'http://localhost:8000'; // FastAPI server URL

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private token: string | null = null;

  async register(email: string, fullName: string, password: string) {
    const response = await axios.post(`${API_URL}/users/register`, {
      email,
      full_name: fullName,
      password,
      // role,
    });
    return response.data;
  }

  async login(email: string, password: string) {
    // Create a FormData object to send as form data
    const formData = new FormData();
    formData.append('username', email); // OAuth2PasswordRequestForm expects 'username'
    formData.append('password', password);

    // Set the appropriate headers for form data
    const response = await axios.post(`${API_URL}/users/login`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    this.token = response.data.access_token; // Store the token
    localStorage.setItem('token', response.data.access_token);
    return response.data;
  }

  // Method to retrieve Authorization headers with the Bearer token
  private getAuthHeaders() {
    this.token = localStorage.getItem('token');
    return this.token ? { Authorization: `Bearer ${this.token}` } : {};
  }

  // Example method to demonstrate usage of `getAuthHeaders` in an authenticated request
  async getUserProfile() {
    const response = await axios.get(`${API_URL}/users/profile`, {
      headers: this.getAuthHeaders(), // Use the token in headers
    });
    return response.data;
  }

  async uploadImage(file: File) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(`${API_URL}/upload`, formData, {
      headers: {
        ...this.getAuthHeaders(),
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  }

  async getImages() {
    const response = await axios.get(`${API_URL}/upload`, {
      headers: this.getAuthHeaders(), // Use the token in headers
    });
    return response.data;
  }

  async processImage(imageId: number) {
    try {
      const response = await axios.post(`${API_URL}/process/${imageId}`, {}, {
        headers: this.getAuthHeaders(), // Include the headers here
      });
      return response.data;
    } catch (error) {
      // Handle the error as needed
      console.error("Error processing image:", error);
      throw error; // You can rethrow or handle the error based on your requirements
    }
  }

  async deleteImage(imageId: number) {
    const response = await axios.delete(`${API_URL}/upload/${imageId}`, {
      headers: this.getAuthHeaders(), // Use the token in headers
    });
    return response.data;
  }

  async getProcessedImages(originalImageId: number) {
    const response = await axios.get(`${API_URL}/process/${originalImageId}`, {
      headers: this.getAuthHeaders(), // Use the token in headers
    });
    return response.data;
  }

  async searchImages(query: string): Promise<any[]> {
    try {
      const response = await axios.get(`${API_URL}/search`, {
        headers: this.getAuthHeaders(), // Use the token in headers
        params: { query },
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching search results:', error);
      throw error;
    }
  }
}
