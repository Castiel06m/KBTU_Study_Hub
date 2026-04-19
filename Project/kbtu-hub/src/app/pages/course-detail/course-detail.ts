import { Component, OnInit, ChangeDetectorRef } from '@angular/core'; 
import { CommonModule } from '@angular/common'; 
import { ActivatedRoute, RouterModule } from '@angular/router';
import { Api } from '../../services/api';
import { Course } from '../../models/course.model';

@Component({
  selector: 'app-course-detail',
  standalone: true,
  imports: [CommonModule, RouterModule], 
  templateUrl: './course-detail.html',
  styleUrl: './course-detail.css'
})
export class CourseDetail implements OnInit {
  course: Course | null = null;

  constructor(
    private route: ActivatedRoute,
    private api: Api,
    private cdr: ChangeDetectorRef 
  ) {}

  ngOnInit() {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.api.getCourseById(id).subscribe({
        next: (data) => {
          this.course = data;
          console.log('Данные курса загружены:', data);
          this.cdr.detectChanges(); // Принудительно обновляем экран
        },
        error: (err) => console.error(err)
      });
    }
  }
}