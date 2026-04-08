import { Routes } from '@angular/router';
import { Home } from './pages/home/home';
import { Login } from './pages/login/login';
import { CourseDetail } from './pages/course-detail/course-detail';

export const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'home', component: Home },
  { path: 'login', component: Login },
  { path: 'course/:id', component: CourseDetail }, // Динамический роут
  { path: '**', redirectTo: 'home' } // Если путь не найден
];