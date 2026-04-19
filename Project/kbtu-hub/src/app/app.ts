import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Api } from './services/api';


@Component({
  selector: 'app-root',
  imports: [RouterOutlet, CommonModule, RouterLink],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('kbtu-hub');

  constructor(public api: Api, private router: Router) {}

  isAuthPage() {
    const url = this.router.url;
    return url === '/login' || url === '/register' || url === '/';
  }

  logout() {
    this.api.logout();
    localStorage.removeItem('access');
    this.router.navigate(['/login']);
  }
}
