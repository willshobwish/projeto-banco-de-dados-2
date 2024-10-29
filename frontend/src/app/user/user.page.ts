import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';
import { Router } from '@angular/router';
@Component({
  selector: 'app-user',
  templateUrl: './user.page.html',
  styleUrls: ['./user.page.scss'],
})
export class UserPage implements OnInit {
  userData: any;

  constructor(private apiService: ApiService, private router: Router) {}

  async ionViewWillEnter() {
    this.loadUserProfile(); // Load user profile when the view is about to enter
  }

  async fetchUserProfile() {
    try {
      this.userData = await this.apiService.getUserProfile(); // Fetch user data
    } catch (error) {
      console.error('Failed to fetch user profile:', error);
      // Redirect to login if there's an error fetching the profile
      this.router.navigate(['/login']);
    }
  }

  loadUserProfile() {
    this.fetchUserProfile(); // Call the fetchUserProfile method
  }

  logout() {
    localStorage.removeItem('token'); // Remove token on logout
    this.router.navigate(['/login']); // Navigate to the login page
  }
  
  async ngOnInit() {
    // this.loadUserProfile(); // Load user profile when the component initializes
  }
}
