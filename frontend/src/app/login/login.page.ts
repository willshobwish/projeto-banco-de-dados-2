import { Component } from '@angular/core';
import { AuthService } from 'src/services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage {
  email: string = '';
  password: string = '';

  constructor(public authService: AuthService, private router: Router) {}

  async login() {
    try {
      await this.authService.login(this.email, this.password);
      this.router.navigate(['/tabs']);
    } catch (error) {
      console.log('Login failed', error);
    }
  }
}
