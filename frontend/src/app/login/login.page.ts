import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';
import { AlertController } from '@ionic/angular';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage implements OnInit {

  email = '';
  password = '';

  constructor(private apiService: ApiService, private alertController: AlertController) {}

  async login() {
    try {
      const result = await this.apiService.login(this.email, this.password);
      const alert = await this.alertController.create({
        header: 'Login Successful',
        message: `Welcome ${result.fullName}!`,
        buttons: ['OK'],
      });
      await alert.present();
      // Redirect to the main page or dashboard after successful login
    } catch (error) {
      const alert = await this.alertController.create({
        header: 'Login Failed',
        message: 'Incorrect email or password.',
        buttons: ['OK'],
      });
      await alert.present();
    }
  }

  ngOnInit() {
  }

}
