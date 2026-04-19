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
        // Сохраняем токен в память браузера
        localStorage.setItem('access', res.access);
        localStorage.setItem('refresh', res.refresh);
        console.log('Успешный вход!');
        this.router.navigate(['/home']); // Переходим на главную
      },
      error: (err) => {
        alert('Ошибка входа: проверь логин и пароль');
        console.error(err);
      }
    });
  }
}