// src/app/services/image.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
// import { UploadResponse } from './upload-response.interface'; // Adjust path as necessary
// src/app/services/image.service.ts
export interface UploadResponse {
    filename: string; // or other properties you expect
  }
  
@Injectable({
  providedIn: 'root'
})
export class ImageUploadService {
  private apiUrl = 'your_api_endpoint'; // Replace with your actual API endpoint

  constructor(private http: HttpClient) {}

  uploadImage(file: File): Observable<UploadResponse> {
    const formData = new FormData();
    formData.append('image', file);

    return this.http.post<UploadResponse>(this.apiUrl, formData);
  }
}
