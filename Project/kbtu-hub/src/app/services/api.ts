import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Course, Guild } from '../models/course.model';

export interface LoginResponse {
  access: string;
  refresh: string;
}

@Injectable({
  providedIn: 'root',
})
export class Api {
  private BASE_URL = 'http://127.0.0.1:8000/api';

  constructor(private http: HttpClient) {}

  getCourses(): Observable<Course[]> {
    return this.http.get<Course[]>(`${this.BASE_URL}/courses/`);
  }

  login(credentials: any): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.BASE_URL}/login/`, credentials);
  }

  logout() {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
      // Можно добавить редирект на логин прямо здесь или в компоненте
  }

  isLoggedIn(): boolean {
    return !!localStorage.getItem('access');
  }

  getCourseById(id: number | string): Observable<Course> {
    return this.http.get<Course>(`${this.BASE_URL}/courses/${id}/`);
  }
  
  register(userData: any): Observable<any> {
    return this.http.post(`${this.BASE_URL}/users/register/`, userData);
  } 

  getGuilds(): Observable<Guild[]> {
    return this.http.get<Guild[]>(`${this.BASE_URL}/guilds/`);
  }

  joinGuild(guildId: number): Observable<any> {
    return this.http.post(`${this.BASE_URL}/guilds/${guildId}/join/`, {});
  }

  addComment(courseId: number, text: string): Observable<any> {
    return this.http.post(`${this.BASE_URL}/courses/${courseId}/comment/`, { text });
  }
}



