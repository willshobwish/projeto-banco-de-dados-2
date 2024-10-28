import { Component, OnInit } from '@angular/core';
import { ImageUploadService, UploadResponse } from '../services/image.service';
import { AlertController } from '@ionic/angular';
import { firstValueFrom } from 'rxjs';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.page.html',
  styleUrls: ['./upload.page.scss'],
})
export class UploadPage implements OnInit {
  selectedFile: File | null = null;

  constructor(
    private imageUploadService: ImageUploadService,
    private alertController: AlertController
  ) {}

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files?.length) {
      this.selectedFile = input.files[0];
    }
  }

  async uploadImage() {
    if (this.selectedFile) {
      try {
        // Use firstValueFrom and assert that the result is not undefined
        const result = await firstValueFrom(this.imageUploadService.uploadImage(this.selectedFile));
        if (result) { // Check if result is defined
          const alert = await this.alertController.create({
            header: 'Upload Successful',
            message: `Image uploaded as ${result.filename}`,
            buttons: ['OK'],
          });
          await alert.present();
        } else {
          // Handle the case where result is undefined
          const alert = await this.alertController.create({
            header: 'Upload Failed',
            message: 'Image upload returned no result.',
            buttons: ['OK'],
          });
          await alert.present();
        }
      } catch (error) {
        const alert = await this.alertController.create({
          header: 'Upload Failed',
          message: 'Could not upload image. Try again later.',
          buttons: ['OK'],
        });
        await alert.present();
      }
    }
  }
  ngOnInit() {}
}
