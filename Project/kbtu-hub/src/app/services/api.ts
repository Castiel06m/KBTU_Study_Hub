import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Category, Course, Guild, LessonCreate } from '../models/course.model';


export interface UserProfile {
  id: number;
  username: string;
  role: 'student' | 'teacher';
}

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

  getMessages(guildId: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.BASE_URL}/guilds/${guildId}/messages/`);
  }

  sendMessage(guildId: number, content: string, isUrgent: boolean, file: File | null): Observable<any> {
    const formData = new FormData();
    formData.append('content', content);
    formData.append('is_urgent', String(isUrgent));
    
    if (file) {
      formData.append('file', file); 
    }

    return this.http.post(`${this.BASE_URL}/guilds/${guildId}/messages/`, formData);
  }

  createGuild(guildData: any): Observable<Guild> {
    return this.http.post<Guild>(`${this.BASE_URL}/guilds/`, guildData);
  }

  addComment(courseId: number, text: string): Observable<any> {
    return this.http.post(`${this.BASE_URL}/courses/${courseId}/comment/`, { text });
  }

  enrollInCourse(courseId: number): Observable<any> {
    return this.http.post(`${this.BASE_URL}/courses/enroll/`, { course: courseId });
  }

  getUserProfile(): Observable<UserProfile> {
    return this.http.get<UserProfile>(`${this.BASE_URL}/users/me/`);
  }

  getUserRole(): string | null {
    return localStorage.getItem('user_role');
  }

  getCategories(): Observable<Category[]> {
    return this.http.get<Category[]>(`${this.BASE_URL}/categories/`);
  }

  createCourse(courseData: any): Observable<Course> {
    return this.http.post<Course>(`${this.BASE_URL}/courses/`, courseData);
  }

  createLesson(lessonData: LessonCreate): Observable<any> {
    const formData = new FormData();
    formData.append('title', lessonData.title);
    formData.append('content', lessonData.content);
    formData.append('course', String(lessonData.course));
    
    if (lessonData.order) formData.append('order', String(lessonData.order));
    if (lessonData.video_url) formData.append('video_url', lessonData.video_url);
    if (lessonData.file) formData.append('file', lessonData.file);

    return this.http.post(`${this.BASE_URL}/lessons/`, formData);
  }
}



