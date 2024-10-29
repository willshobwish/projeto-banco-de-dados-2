import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';
import { AlertController } from '@ionic/angular';
import { Router } from '@angular/router';
@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage implements OnInit {
  email = '';
  password = '';

  constructor(
    private apiService: ApiService,
    private alertController: AlertController,
    private router: Router
  ) {}

  async login() {
    try {
      const result = await this.apiService.login(this.email, this.password);
      const alert = await this.alertController.create({
        header: 'Login Successful',
        message: 'You are now logged in!',
        buttons: ['OK'],
      });
      await alert.present();
      this.router.navigate(['tabs/user']); // Navigate to the User Profile page
    } catch (error) {
      const alert = await this.alertController.create({
        header: 'Login Failed',
        message: 'Incorrect email or password.',
        buttons: ['OK'],
      });
      await alert.present();
    }
  }
  ngOnInit() {}
}
