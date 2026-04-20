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
  isEnrolled: boolean = false;

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
          this.isEnrolled = data.is_enrolled;
          // console.log('Данные курса загружены:', data);
          this.cdr.detectChanges(); // Принудительно обновляем экран
        },
        error: (err) => console.error(err)
      });
    }
  }

  enroll() {
    if (!this.course) return;

    this.api.enrollInCourse(this.course.id).subscribe({
      next: (res) => {
        alert('Вы успешно записаны на курс!');
        this.isEnrolled = true; 
        this.cdr.detectChanges();
      },
      error: (err) => {
        const msg = err.error?.message || 'Ошибка при записи';
        alert(msg);
        if (msg.includes('уже записаны')) {
            this.isEnrolled = true;
            this.cdr.detectChanges();
        }
      }
    });
  }
}