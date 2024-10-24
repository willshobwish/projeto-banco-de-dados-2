import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Storage } from '@ionic/storage-angular';
import { Observable,firstValueFrom } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:8000'; // FastAPI backend URL
  private tokenKey = 'auth-token'; // Storage key for JWT token

  constructor(private http: HttpClient, private storage: Storage) {
    this.storage.create(); // Initialize Ionic storage
  }
  registerUser(email: string, password: string, name: string, file: File | null): Observable<any> {
    const formData = new FormData();
    formData.append('email', email);
    formData.append('password', password);
    formData.append('name', name);
    if (file) {
      formData.append('file', file);
    }

    return this.http.post(`${this.apiUrl}/users/`, formData);
  }

// Login and get JWT
async login(email: string, password: string) {
  try {
    const res: any = await firstValueFrom(this.http.post(`${this.apiUrl}/token`, {
      username: email,
      password: password
    }));
    await this.storage.set(this.tokenKey, res.access_token); // Store JWT
    return res;
  } catch (err) {
    console.error("Login failed:", err);
  }
}


  // Check if user is authenticated
  async isAuthenticated(): Promise<boolean> {
    const token = await this.storage.get(this.tokenKey);
    return !!token;
  }

  // Get current user information using JWT
  async getUserInfo() {
    const token = await this.storage.get(this.tokenKey);
    return this.http.get(`${this.apiUrl}/users/me`, {
      headers: { 'Authorization': `Bearer ${token}` }
    }).toPromise();
  }

  // Logout user
  async logout() {
    await this.storage.remove(this.tokenKey);
  }
}
