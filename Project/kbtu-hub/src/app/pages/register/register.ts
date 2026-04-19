import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { Api } from '../../services/api';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule], 
  templateUrl: './register.html', 
  styleUrl: './register.css'
})
export class Register {
  userData = {
    username: '',
    email: '',
    password: '',
    role: 'student' // по дефолту студент
  };

  errorMessage: string = '';

  constructor(private api: Api, private router: Router) {}

  onRegister() {
    this.api.register(this.userData).subscribe({
      next: (response) => {
        console.log('Успех:', response);
        this.router.navigate(['/login']);
      },
      error: (err) => {
        console.error('Ошибка регистрации:', err);
        this.errorMessage = 'Ошибка при создании аккаунта. Возможно, логин занят.';
      }
    });
  }
}