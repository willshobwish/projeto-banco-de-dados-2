import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';
import { AlertController } from '@ionic/angular';

@Component({
  selector: 'app-register',
  templateUrl: './register.page.html',
  styleUrls: ['./register.page.scss'],
})
export class RegisterPage implements OnInit {
  email = '';
  fullName = '';
  password = '';
  role = 'user';

  constructor(
    private apiService: ApiService,
    private alertController: AlertController
  ) {}

  async register() {
    try {
      const result = await this.apiService.register(
        this.email,
        this.fullName,
        this.password,
        this.role
      );
      const alert = await this.alertController.create({
        header: 'Registration Successful',
        message: `User ${result.email} registered!`,
        buttons: ['OK'],
      });
      await alert.present();
    } catch (error) {
      const alert = await this.alertController.create({
        header: 'Registration Failed',
        message: 'Please check your information and try again.',
        buttons: ['OK'],
      });
      await alert.present();
    }
  }
  ngOnInit() {}
}
