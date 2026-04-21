import { Component, OnInit, ChangeDetectorRef } from '@angular/core'; 
import { CommonModule } from '@angular/common'; 
import { ActivatedRoute, RouterModule } from '@angular/router';
import { Api } from '../../services/api';
import { Course, LessonCreate } from '../../models/course.model';
import { FormsModule } from '@angular/forms';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser'; 

@Component({
  selector: 'app-course-detail',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule], 
  templateUrl: './course-detail.html',
  styleUrl: './course-detail.css'
})
export class CourseDetail implements OnInit {
  course: Course | null = null;
  isEnrolled: boolean = false;
  isAuthor: boolean = false;
  selectedFile: File | null = null;
  commentText = '';
  expandedLessonId: number | null = null;

  newLesson: LessonCreate = {
    title: '',
    content: '',
    course: 0,
    video_url: ''
  };

  constructor(
    private route: ActivatedRoute,
    private api: Api,
    private cdr: ChangeDetectorRef,
    private sanitizer: DomSanitizer 
  ) {}

  ngOnInit() {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.api.getCourseById(id).subscribe({
        next: (data) => {
          this.course = data;
          this.isEnrolled = data.is_enrolled;
          this.newLesson.course = data.id;
          this.checkAuthorStatus();
          // console.log('Данные курса загружены:', data);
          this.cdr.detectChanges(); // Принудительно обновляем экран
        },
        error: (err) => console.error(err)
      });
    }
  }

  loadCourse(id: string | number) {
    this.api.getCourseById(id).subscribe({
      next: (data) => {
        this.course = data;
        this.isEnrolled = data.is_enrolled;
        this.newLesson.course = data.id;
        this.checkAuthorStatus();
        this.cdr.detectChanges();
      }
    });
  }

  checkAuthorStatus() {
    if (this.api.isLoggedIn() && this.course) {
      this.api.getUserProfile().subscribe({
        next: (profile) => {
          this.isAuthor = (Number(profile.id) === Number(this.course?.author));
          console.log('Является автором?', this.isAuthor);
          this.cdr.detectChanges();
        },
        error: (err) => console.error('Ошибка загрузки профиля', err)
      });
    }
  }

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
  }

  addLesson() {
    if (!this.newLesson.title) return;

    const dataToSend = { ...this.newLesson, file: this.selectedFile };

    this.api.createLesson(dataToSend).subscribe({
      next: () => {
        alert('Урок добавлен!');
        this.loadCourse(this.course!.id); 
        this.resetForm();
      },
      error: () => alert('Ошибка при создании')
    });
  }

  resetForm() {
    this.newLesson = { title: '', content: '', course: this.course?.id || 0, video_url: '' };
    this.selectedFile = null;
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

  sendComment() {
    if (!this.commentText.trim() || !this.course) {
      alert("Напишите что-нибудь в отзыве!");
      return;
    }

    this.api.addComment(this.course.id, this.commentText).subscribe({
      next: (newComment) => {
        if (this.course) {
          this.course.comments.push(newComment);
        }
        this.commentText = ''; 
        this.cdr.detectChanges(); 
      },
      error: (err) => {
        console.error(err);
        alert("Ошибка при отправке комментария. Возможно, вы не авторизованы.");
      }
    });
  }

  toggleLesson(id: number) {
    this.expandedLessonId = this.expandedLessonId === id ? null : id;
  }

  getSafeVideoUrl(url: string): SafeResourceUrl | null {
    if (!url) return null;
    // из обычной ссылки в embed-ссылку
    const videoId = url.split('v=')[1] || url.split('/').pop();
    const embedUrl = `https://www.youtube.com/embed/${videoId}`;
    return this.sanitizer.bypassSecurityTrustResourceUrl(embedUrl);
  }
}