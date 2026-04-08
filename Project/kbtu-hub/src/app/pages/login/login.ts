import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login',
  imports: [CommonModule, FormsModule],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {
  loginData = {
    username: "",
    password: "",
  }

  onSubmit(){
    // КРИТЕРИЙ: (click) event, который позже триггернет API
    console.log('Trying to login with:', this.loginData);
    // вызов AuthService
  }
}
