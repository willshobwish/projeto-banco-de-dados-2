import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';

const API_URL = 'http://localhost:8000';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private token: string | null = null;

  constructor(private http: HttpClient, private router: Router) {}

  login(email: string, password: string) {
    return this.http
      .post(`${API_URL}/auth/login`, { username: email, password })
      .subscribe((response: any) => {
        this.token = response.access_token;
        if (this.token) {
          localStorage.setItem('token', this.token);
      }
        this.router.navigate(['/protected']);
      });
  }

  isLoggedIn(): boolean {
    return !!localStorage.getItem('token');
  }

  logout() {
    localStorage.removeItem('token');
    this.token = null;
    this.router.navigate(['/login']);
  }

  getToken(): string | null {
    return localStorage.getItem('token');
  }
}
