import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-processed-images',
  templateUrl: './processed-images.page.html',
  styleUrls: ['./processed-images.page.scss'],
})
export class ProcessedImagesPage implements OnInit {

  processedImages: any[] = []; // Store processed images here
  originalImageId!: number; // ID of the original image

  constructor(private apiService: ApiService, private route: ActivatedRoute) {}

  async ngOnInit() {
    // Get the original image ID from the route parameters
    this.originalImageId = Number(this.route.snapshot.paramMap.get('image_id'));
    await this.loadProcessedImages();
  }

  async loadProcessedImages() {
    try {
      this.processedImages = await this.apiService.getProcessedImages(this.originalImageId);
    } catch (error) {
      console.error('Failed to fetch processed images:', error);
    }
  }

}
