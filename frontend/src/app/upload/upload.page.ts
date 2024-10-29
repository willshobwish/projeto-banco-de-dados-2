import { Component, OnInit } from '@angular/core';
import { AlertController } from '@ionic/angular';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.page.html',
  styleUrls: ['./upload.page.scss'],
})
export class UploadPage implements OnInit {
  selectedFile: File | null = null;

  constructor(
    private apiService: ApiService,
    private alertController: AlertController
  ) {}

  onFileSelected(event: any) {
    const file: File = event.target.files[0];
    this.selectedFile = file;
  }

  async uploadImage(event: Event) {
    event.preventDefault();
    if (!this.selectedFile) {
      return;
    }

    try {
      const result = await this.apiService.uploadImage(this.selectedFile);
      const alert = await this.alertController.create({
        header: 'Upload Successful',
        message: 'Your image was uploaded successfully!',
        buttons: ['OK'],
      });
      await alert.present();
    } catch (error) {
      const alert = await this.alertController.create({
        header: 'Upload Failed',
        message: 'Could not upload the image. Please try again.',
        buttons: ['OK'],
      });
      await alert.present();
    }
  }

  ngOnInit() {}
}
