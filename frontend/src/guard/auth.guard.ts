import { Injectable, Injector } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { AuthService } from 'src/services/auth.service';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(private injector: Injector, private router: Router) {}

  async canActivate(): Promise<boolean> {
    const authService = this.injector.get(AuthService); // Use Injector
    const isAuthenticated = await authService.isAuthenticated();
    
    if (!isAuthenticated) {
      this.router.navigate(['/login']);
      return false;
    }
    return true;
  }
}
