import { Component } from '@angular/core';
import { CommonModule } from '@angular/common'; // Обязательно для standalone
import { RouterModule } from '@angular/router';
import { Course } from '../../models/course.model';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home {

  // Пока не готов бэк
  courses: Course[] = [
    { id: 1, title: 'Web Development', code: 'CSCI 1202', description: 'Angular + Django' },
    { id: 2, title: 'Calculus I', code: 'MATH 1101', description: 'Limits, Derivatives' },
    { id: 3, title: 'Physics', code: 'PHYS 1101', description: 'Mechanics' },
    { id: 4, title: 'Database Systems', code: 'CSCI 2101', description: 'SQL & NoSQL' },
  ];
  
}
