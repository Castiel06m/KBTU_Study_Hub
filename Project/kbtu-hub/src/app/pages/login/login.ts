import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { Api } from '../../services/api';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink], 
  templateUrl: './login.html',
  styleUrl: './login.css'
})
export class Login {
  loginData = {
    username: '',
    password: ''
  };

  constructor(private api: Api, private router: Router) {}

  onLogin() {
    this.api.login(this.loginData).subscribe({
      next: (res) => {
        localStorage.setItem('access', res.access);
        localStorage.setItem('refresh', res.refresh);

        this.api.getUserProfile().subscribe({
          next: (profile) => {
            localStorage.setItem('user_role', profile.role); 
            console.log('Успешный вход, роль:', profile.role);
            this.router.navigate(['/home']);
          },
          error: (err) => {
            console.error('Не удалось получить профиль', err);
            this.router.navigate(['/home']);
          }
        });
      },
      error: (err) => {
        alert('Ошибка входа: проверь логин и пароль');
      }
    });
  }
}