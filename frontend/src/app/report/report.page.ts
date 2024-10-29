import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';
import { Router } from '@angular/router';
// import { format } from 'date-fns'; // Optional if using date-fns for formatting
import { AlertController } from '@ionic/angular'; // Import AlertController

export interface ImageResponse {
  id: number;
  file_path: string;
  is_processed: boolean;
  filename: string;
  created_at: string;
  updated_at: string;
}
@Component({
  selector: 'app-report',
  templateUrl: './report.page.html',
  styleUrls: ['./report.page.scss'],
})
export class ReportPage implements OnInit {
  userImages: ImageResponse[] = []; // Store user images here with the interface type

  constructor(
    private apiService: ApiService,
    private router: Router,
    private alertController: AlertController
  ) {}

  async ionViewWillEnter() {
    await this.loadUserImages(); // Load user images when the view is about to enter
  }

  async ngOnInit() {
    await this.loadUserImages(); // Load user images on component initialization
  }

  async processImage(imageId: number) {
    try {
      await this.apiService.processImage(imageId); // Process the image

      // Show success alert
      const alert = await this.alertController.create({
        header: 'Success',
        message: 'Image processed successfully!',
        buttons: ['OK'],
      });
      await alert.present();

      // Reload the page after the alert is dismissed
      alert.onDidDismiss().then(() => {
        this.loadUserImages(); // Call method to reload images
      });
    } catch (error) {
      console.error('Error processing image:', error);
      // Handle error notification if needed
      const alert = await this.alertController.create({
        header: 'Error',
        message: 'Failed to process image.',
        buttons: ['OK'],
      });
      await alert.present();
    }
  }

  getFilename(filePath: string): string {
    return filePath.split('/').pop() || filePath; // Adjust for backslashes if needed
  }

  async deleteImage(imageId: number) {
    try {
      await this.apiService.deleteImage(imageId);
      this.userImages = this.userImages.filter((image) => image.id !== imageId); // Remove image from UI
    } catch (error) {
      console.error('Failed to delete image:', error);
    }
  }
  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleString(); // Adjust format here, or use date-fns if installed
  }
  async loadUserImages() {
    try {
      this.userImages = await this.apiService.getImages(); // Fetch user images

      // Optionally, you can map the API response to ensure it fits the ImageResponse type
      // const userId = this.apiService.getUserProfile().id

      this.userImages = this.userImages.map((image: any) => ({
        id: image.id,
        file_path: image.file_path,
        is_processed: image.is_processed,
        filename: this.getFilename(image.file_path),
        created_at: this.formatDate(image.created_at),
        updated_at: this.formatDate(image.updated_at),
      }));
    } catch (error) {
      console.error('Failed to fetch user images:', error);
      // Optionally, redirect to login if there's an error
      this.router.navigate(['/login']);
    }
  }
}
