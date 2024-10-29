// src/app/services/auth.guard.ts
import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import { ApiService } from './api.service';

@Injectable({
  providedIn: 'root',
})
export class AuthGuard implements CanActivate {
  constructor(private apiService: ApiService, private router: Router) {}

  async canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Promise<boolean> {
    const token = localStorage.getItem('token'); // Get token from local storage

    if (token) {
      // Optionally verify if the token is still valid
      return true; // User is authenticated
    } else {
      // Redirect to login if not authenticated
      this.router.navigate(['/login']);
      return false; // User is not authenticated
    }
  }
}
