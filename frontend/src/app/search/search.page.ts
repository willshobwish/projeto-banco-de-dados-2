import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';
import { LoadingController, ToastController } from '@ionic/angular';
@Component({
  selector: 'app-search',
  templateUrl: './search.page.html',
  styleUrls: ['./search.page.scss'],
})
export class SearchPage implements OnInit {
  query: string = '';
  results: any[] = [];
  submitted: boolean = false;

  constructor(
    private apiSerive: ApiService,
    private loadingController: LoadingController,
    private toastController: ToastController
  ) {}

  async searchImages() {
    this.submitted = true;

    const loading = await this.loadingController.create({
      message: 'Searching...',
    });
    await loading.present();

    try {
      this.results = await this.apiSerive.searchImages(this.query);
    } catch (error) {
      const toast = await this.toastController.create({
        message: 'Error fetching search results. Please try again.',
        duration: 2000,
        color: 'danger',
      });
      await toast.present();
    } finally {
      await loading.dismiss();
    }
  }
  ngOnInit() {
  }

}
