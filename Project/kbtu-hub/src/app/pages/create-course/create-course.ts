import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Api } from '../../services/api';
import { Router } from '@angular/router';
import { Category } from '../../models/course.model';

@Component({
  selector: 'app-create-course',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './create-course.html',
  styleUrl: './create-course.css'
})
export class CreateCourse implements OnInit {
  categories: Category[] = [];
  courseData = {
    title: '',
    description: '',
    category: null
  };

  constructor(private api: Api, private router: Router) {}

  ngOnInit() {
    this.api.getCategories().subscribe(data => this.categories = data);
  }

  onSubmit() {
    this.api.createCourse(this.courseData).subscribe({
      next: (res) => {
        alert('Курс успешно создан!');
        this.router.navigate(['/course', res.id]); 
      },
      error: (err) => alert('Ошибка при создании курса')
    });
  }
}