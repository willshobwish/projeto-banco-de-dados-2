import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';
import { AlertController } from '@ionic/angular';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.page.html',
  styleUrls: ['./register.page.scss'],
})
export class RegisterPage implements OnInit {
  email = '';
  fullName = '';
  password = '';
  // role = 'user';

  constructor(
    private apiService: ApiService,
    private alertController: AlertController,
    private router:Router
  ) {}

  async register() {
    try {
      const result = await this.apiService.register(
        this.email,
        this.fullName,
        this.password,
        
      );
      const alert = await this.alertController.create({
        header: 'Registration Successful',
        message: `User ${result.email} registered!`,
        buttons: ['OK'],
      });
      await alert.present();
      this.router.navigate(['/login'])
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
