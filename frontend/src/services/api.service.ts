import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private apiUrl = 'http://127.0.0.1:8000/inference/';  // Example API URL

  constructor(private http: HttpClient) { }

  // Method to get data from an endpoint
  getData(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/posts`);
  }

  // Method to post data to an endpoint
  postData(data: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/posts`, data);
  }
}
