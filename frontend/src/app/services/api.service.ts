import { Injectable } from '@angular/core';
import axios from 'axios';

const API_URL = 'http://localhost:8000'; // FastAPI server URL

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  async register(email: string, fullName: string, password: string, role: string) {
    const response = await axios.post(`${API_URL}/users/`, {
      email,
      full_name: fullName,
      password,
      role,
    });
    return response.data;
  }

  async login(email: string, password: string) {
    const response = await axios.post(`${API_URL}/auth/login`, {
      email,
      password,
    });
    return response.data;
  }
}
