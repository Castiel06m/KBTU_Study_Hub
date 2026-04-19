import { Component, OnInit, ChangeDetectorRef} from '@angular/core';
import { CommonModule } from '@angular/common'; // Обязательно для standalone
import { RouterModule } from '@angular/router';
import { Course } from '../../models/course.model';
import { Api } from '../../services/api';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home implements OnInit {
  courses: Course[] = []; 

  constructor(private apiService: Api, private cdr: ChangeDetectorRef) {}

  ngOnInit() {
    this.loadCourses();
  }

  loadCourses() {
    this.apiService.getCourses().subscribe({
      next: (data: Course[]) => {
        this.courses = data;
        // Сразу проверяем, что в самой переменной класса теперь есть данные
        console.log('Проверка внутри subscribe:', this.courses.length);
        
        // ПРИНУДИТЕЛЬНО говорим Angular: "Эй, данные изменились!"
        this.cdr.detectChanges();
      },
      error: (err) => console.error(err)
    });
  }
  
  
}
