import { Routes } from '@angular/router';
import { Home } from './pages/home/home';
import { Login } from './pages/login/login';
import { Register } from './pages/register/register'; 
import { CourseDetail } from './pages/course-detail/course-detail';
import { GuildsList } from './pages/guilds-list/guilds-list'; 
import { CreateCourse } from './pages/create-course/create-course';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: Login },
  { path: 'register', component: Register }, 
  { path: 'home', component: Home },
  { path: 'course/:id', component: CourseDetail },
  { path: 'guilds', component: GuildsList }, 
  { path: 'create-course', component: CreateCourse },
  { path: '**', redirectTo: 'home' }
];