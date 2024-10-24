import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Storage } from '@ionic/storage-angular';
import { Observable, firstValueFrom } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private apiUrl = 'http://localhost:8000'; // FastAPI backend URL
  private tokenKey = 'auth-token'; // Storage key for JWT token

  constructor(private http: HttpClient, private storage: Storage) {
    this.storage.create(); // Initialize Ionic storage
  }

  /**
   * Registers a new user with email, password, name, and an optional file.
   * @param email User's email
   * @param password User's password
   * @param name User's name
   * @param file Optional image file to upload
   * @returns Observable of the HTTP response
   */
  registerUser(email: string, password: string, name: string): Observable<any> {
    const formData = new FormData();
    formData.append('email', email);
    formData.append('password', password);
    formData.append('name', name);
    // if (file) {
    //   formData.append('file', file);
    // }

    return this.http.post(`${this.apiUrl}/users/`, formData);
  }

  /**
   * Logs in a user and retrieves the JWT.
   * @param email User's email
   * @param password User's password
   * @returns A promise resolving to the server response
   */
  async login(email: string, password: string): Promise<any> {
    try {
      const res: any = await firstValueFrom(this.http.post(`${this.apiUrl}/token`, {
        username: email,
        password: password,
      }));
      await this.storage.set(this.tokenKey, res.access_token); // Store JWT
      return res;
    } catch (err) {
      console.error('Login failed:', err);
      throw new Error('Invalid credentials');
    }
  }

  /**
   * Checks if the user is authenticated by verifying the presence of the token.
   * @returns A promise resolving to true if authenticated, otherwise false
   */
  async isAuthenticated(): Promise<boolean> {
    const token = await this.storage.get(this.tokenKey);
    return !!token;
  }

  /**
   * Retrieves the current user's information using the JWT.
   * @returns A promise resolving to the user's information
   */
  async getUserInfo(): Promise<any> {
    const token = await this.storage.get(this.tokenKey);
    try {
      return await this.http.get(`${this.apiUrl}/users/me`, {
        headers: { Authorization: `Bearer ${token}` },
      }).toPromise();
    } catch (error) {
      console.error('Failed to get user info:', error);
      throw error; // Re-throw to handle in component if needed
    }
  }

  /**
   * Logs out the user by removing the JWT from storage.
   */
  async logout(): Promise<void> {
    await this.storage.remove(this.tokenKey);
  }
}
