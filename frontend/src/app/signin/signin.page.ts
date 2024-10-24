import { Component, OnInit } from '@angular/core';
import { AuthService } from 'src/services/auth.service';
import { Router } from '@angular/router';
@Component({
  selector: 'app-signin',
  templateUrl: './signin.page.html',
  styleUrls: ['./signin.page.scss'],
})
export class SigninPage implements OnInit {
  email: string = '';
  password: string = '';
  confirmPassword: string = '';
  name: string = '';
  selectedFile: File | null = null;
  errorMessage: string = '';

  constructor(private authService: AuthService, private router: Router) {}

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.selectedFile = input.files[0];
    }
  }

  onRegister() {
    if (this.password !== this.confirmPassword) {
      this.errorMessage = 'Passwords do not match!';
      return;
    }

    this.authService
      .registerUser(this.email, this.password, this.name, this.selectedFile)
      .subscribe({
        next: (response) => {
          this.router.navigate(['/tabs/user']); // Redirect to user page after registration
        },
        error: (err) => {
          this.errorMessage = 'Registration failed!';
        },
      });
  }
  ngOnInit() {}
}
